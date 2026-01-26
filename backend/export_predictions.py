#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exportador de predicciones de callos para interfaz web.

Este script:
  1. Carga un modelo de segmentación entrenado (UNet++, UNet, DeepLabV3+, etc.).
  2. Ejecuta inferencia sobre todas las imágenes de una carpeta.
  3. Extrae los polígonos de cada componente conectada ≥ min_area.
  4. Genera:
       - web/images/<case_id>.png
       - web/data.js   (const DATA = [...])

USO EJEMPLO:
    python backend/export_predictions.py ^
      --images "D:/PrevencionLesion-UPCH-Monitoreo/entrenamiento_individual_yolo/callos/test/imagenes_originales" ^
      --model-ckpt "D:/PLesion_upch/Fase3_piloto_entrenamientos/callos_unetpp_b4_832_recall/checkpoints/unetpp_effb5_best_Dice.pth" ^
      --out-dir "web" ^
      --architecture "UnetPlusPlus" ^
      --encoder "timm-efficientnet-b5" ^
      --img-long 832 ^
      --crop 832

Para usar otro modelo, cambia --architecture y --encoder según tu modelo entrenado.
"""

import os
import json
from pathlib import Path
import argparse

import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import functional as TF

import segmentation_models_pytorch as smp
from tqdm import tqdm

from scipy import ndimage as ndi
import cv2


# -------------------------------------------------------
# Utilidades
# -------------------------------------------------------

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def list_images(d: str):
    return sorted([str(p) for p in Path(d).glob("*") if p.suffix.lower() in IMG_EXTS])


def stem(p: str):
    return Path(p).stem


def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)
    return p


def pad_to_min_size(img_pil: Image.Image, mask_bool_np: np.ndarray, tw: int, th: int):
    """
    Rellena la imagen hasta (tw, th) usando padding NEGRO (constant=0),
    sin reflect. Así evitamos que se creen "mosaicos" de pies reflejados.
    """
    w, h = img_pil.size
    need_w = max(0, tw - w)
    need_h = max(0, th - h)
    if need_w <= 0 and need_h <= 0:
        return img_pil, mask_bool_np

    pl = need_w // 2
    pr = need_w - pl
    pt = need_h // 2
    pb = need_h - pt

    # Padding negro alrededor
    img_pil = TF.pad(
        img_pil,
        [pl, pt, pr, pb],
        padding_mode="constant",
        fill=0  # negro
    )

    # La máscara (dummy) se rellena con False
    mask_bool_np = np.pad(
        mask_bool_np,
        ((pt, pb), (pl, pr)),
        mode="constant",
        constant_values=False
    )

    return img_pil, mask_bool_np


# -------------------------------------------------------
# Dataset para INFERENCIA (sin máscaras GT)
# -------------------------------------------------------

class InferenceDataset(Dataset):
    def __init__(self, img_dir, img_long=832, crop=832, encoder_name="timm-efficientnet-b5"):
        self.img_paths = list_images(img_dir)
        self.img_long = img_long
        self.crop = crop

        params = smp.encoders.get_preprocessing_params(encoder_name)
        self.mean = torch.tensor(params["mean"]).view(3, 1, 1)
        self.std = torch.tensor(params["std"]).view(3, 1, 1)

    def __len__(self):
        return len(self.img_paths)

    def _resize_keep_ratio(self, img, target_long):
        w, h = img.size
        if max(w, h) == target_long:
            return img

        s = target_long / float(max(w, h))
        nw, nh = int(round(w * s)), int(round(h * s))
        return img.resize((nw, nh), Image.BILINEAR)

    def __getitem__(self, idx):
        ip = self.img_paths[idx]
        img = Image.open(ip).convert("RGB")

        # Redimensionar + pad + crop centrado
        img = self._resize_keep_ratio(img, self.img_long)
        dummy_mask = np.zeros((img.size[1], img.size[0]), dtype=bool)
        img, dummy_mask = pad_to_min_size(img, dummy_mask, self.crop, self.crop)

        w, h = img.size
        if w > self.crop or h > self.crop:
            l = (w - self.crop) // 2
            t = (h - self.crop) // 2
            img = img.crop((l, t, l + self.crop, t + self.crop))

        img_raw = TF.to_tensor(img)  # 0..1
        x = (img_raw - self.mean) / self.std
        name = stem(ip)

        return {
            "pixel_values": x.contiguous(),
            "img_raw": img_raw.contiguous(),
            "name": name,
            "orig_path": ip
        }


def collate_fn(batch):
    return {
        "pixel_values": torch.stack([b["pixel_values"] for b in batch], 0),
        "img_raw": torch.stack([b["img_raw"] for b in batch], 0),
        "name": [b["name"] for b in batch],
        "orig_path": [b["orig_path"] for b in batch],
    }


# -------------------------------------------------------
# INFERENCIA + extracción de polígonos
# -------------------------------------------------------

@torch.no_grad()
def run_inference(model, loader, device, out_img_dir, thr=0.30, min_area=0,
                  gate_foot=True, foot_v=0.08):
    model.eval()
    cases = []

    pbar = tqdm(loader, desc="[INFERENCIA]")
    for batch in pbar:
        x = batch["pixel_values"].to(device, non_blocking=True)
        raw = batch["img_raw"].to(device, non_blocking=True)
        names = batch["name"]

        # Inferencia modelo
        with torch.amp.autocast("cuda", enabled=torch.cuda.is_available()):
            logits = model(x)
            prob = torch.sigmoid(logits).squeeze(1)  # (N,H,W)

        pred = (prob >= thr)

        # Gate fuera del pie
        if gate_foot:
            vmax = raw.max(dim=1)[0]
            foot_mask = (vmax > foot_v)
            pred = pred & foot_mask

        pred_np = pred.cpu().numpy()
        raw_uint8 = (raw.cpu().numpy().transpose(0, 2, 3, 1) * 255).astype(np.uint8)

        # Procesar cada imagen del batch
        for i, name in enumerate(names):
            img_arr = raw_uint8[i]
            mask = pred_np[i].astype(np.uint8)

            # Filtrar componentes pequeñas
            if min_area and min_area > 1:
                lbl, num = ndi.label(mask, structure=np.ones((3, 3), np.uint8))
                if num > 0:
                    cnt = np.bincount(lbl.ravel())
                    keep = np.zeros_like(cnt, dtype=bool)
                    keep[0] = False
                    keep[np.where(cnt >= min_area)[0]] = True
                    mask = keep[lbl].astype(np.uint8)

            # Guardar imagen procesada en web/images/
            out_path = os.path.join(out_img_dir, f"{name}.png")
            Image.fromarray(img_arr).save(out_path)

            # Extraer polígonos con OpenCV
            contours, _ = cv2.findContours(
                (mask * 255).astype(np.uint8),
                mode=cv2.RETR_EXTERNAL,
                method=cv2.CHAIN_APPROX_SIMPLE
            )

            lesions = []
            for j, cnt in enumerate(contours, start=1):
                pts = cnt[:, 0, :].tolist()
                if len(pts) < 3:
                    continue
                lesions.append({
                    "id": f"L{j}",
                    "points": pts
                })

            cases.append({
                "case_id": name,
                "image_url": f"images/{name}.png",
                "lesions": lesions
            })

    return cases


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", type=str, required=True,
                    help="Carpeta con imágenes originales (test).")
    ap.add_argument("--model-ckpt", type=str, required=True,
                    help="Ruta al checkpoint .pth del modelo.")
    ap.add_argument("--out-dir", type=str, required=True,
                    help="Carpeta de salida (ej: web).")
    ap.add_argument("--architecture", type=str, default="UnetPlusPlus",
                    help="Arquitectura del modelo: UnetPlusPlus, Unet, DeepLabV3Plus, FPN, PSPNet, etc.")
    ap.add_argument("--encoder", type=str, default="timm-efficientnet-b5",
                    help="Nombre del encoder (ej: timm-efficientnet-b5, resnet34, efficientnet-b4, etc.)")
    ap.add_argument("--img-long", type=int, default=832,
                    help="Tamaño del lado largo para redimensionar (default: 832).")
    ap.add_argument("--crop", type=int, default=832,
                    help="Tamaño del crop cuadrado (default: 832).")
    ap.add_argument("--thr", type=float, default=0.30,
                    help="Umbral de probabilidad para binarizar (default: 0.30).")
    ap.add_argument("--min-area", type=int, default=0,
                    help="Área mínima de píxeles para filtrar componentes (default: 0 = no filtrar).")
    ap.add_argument("--batch-size", type=int, default=2,
                    help="Tamaño del batch para inferencia (default: 2).")
    ap.add_argument("--data-js-name", type=str, default="data.js",
                    help="Nombre del archivo data.js de salida (default: data.js). Útil para comparar modelos.")
    return ap.parse_args()


def main():
    args = parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] CUDA disponible: {torch.cuda.is_available()}")

    # Preparar carpetas
    out_dir = ensure_dir(args.out_dir)
    out_img_dir = ensure_dir(os.path.join(out_dir, "images"))

    # Crear modelo según arquitectura especificada
    print(f"[INFO] Cargando modelo: {args.architecture} con encoder {args.encoder}...")
    
    # Obtener la clase del modelo desde smp
    arch_name = args.architecture
    if not hasattr(smp, arch_name):
        raise ValueError(f"Arquitectura '{arch_name}' no encontrada en segmentation_models_pytorch. "
                        f"Opciones comunes: UnetPlusPlus, Unet, DeepLabV3Plus, FPN, PSPNet, Linknet, PAN")
    
    model_class = getattr(smp, arch_name)
    model = model_class(
        encoder_name=args.encoder,
        encoder_weights=None,  # No cargar pesos pre-entrenados, usaremos el checkpoint
        in_channels=3,
        classes=1
    ).to(device)

    state = torch.load(args.model_ckpt, map_location="cpu")
    
    # Intentar cargar el estado dict de diferentes formas
    if isinstance(state, dict):
        if "model_state_dict" in state:
            model.load_state_dict(state["model_state_dict"], strict=False)
        elif "state_dict" in state:
            model.load_state_dict(state["state_dict"], strict=False)
        else:
            model.load_state_dict(state, strict=False)
    else:
        model.load_state_dict(state, strict=False)
    
    print("[OK] Modelo cargado.")

    # Dataset y loader (usando los parámetros de tamaño especificados)
    ds = InferenceDataset(
        args.images,
        img_long=args.img_long,
        crop=args.crop,
        encoder_name=args.encoder
    )
    dl = DataLoader(
        ds,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=0,
        collate_fn=collate_fn
    )

    # Inferencia
    cases = run_inference(
        model, dl, device, out_img_dir,
        thr=args.thr,
        min_area=args.min_area,
        gate_foot=True,
        foot_v=0.08
    )

    # Guardar data.js
    data_js_path = os.path.join(out_dir, args.data_js_name)
    with open(data_js_path, "w", encoding="utf-8") as f:
        f.write("const DATA = ")
        json.dump(cases, f, indent=2)
        f.write(";")
    print(f"[OK] {args.data_js_name} generado en: {data_js_path}")
    print(f"[OK] {len(cases)} casos exportados.")


if __name__ == "__main__":
    main()