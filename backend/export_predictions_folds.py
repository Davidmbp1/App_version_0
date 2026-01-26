#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exportador de predicciones con FOLDS para interfaz web.
Adaptado para usar la estructura de entrenamiento con k-fold cross-validation.

Este script:
  1. Carga modelos de múltiples folds (ensemble) o un fold específico.
  2. Ejecuta inferencia con Sliding Window (como en predict.py).
  3. Extrae polígonos de lesiones detectadas.
  4. Genera web/images/ y web/data.js para la herramienta de anotación.

USO:
    # Activar entorno virtual primero:
    # .venv\Scripts\activate  (Windows)
    
    # Ensemble (todos los folds):
    python backend/export_predictions_folds.py ^
      --lesion callos ^
      --scenario all_weeks ^
      --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority" ^
      --out-root "D:\PLesion_upch\Fase3_piloto_entrenamientos\Entrenamientos_2026\output" ^
      --web-dir "web" ^
      --arch UnetPlusPlus ^
      --encoder timm-efficientnet-b5 ^
      --fold -1 ^
      --threshold 0.50
    
    # Fold específico:
    python backend/export_predictions_folds.py ^
      --lesion callos ^
      --scenario all_weeks ^
      --consensus-root "..." ^
      --out-root "..." ^
      --web-dir "web" ^
      --arch UnetPlusPlus ^
      --encoder timm-efficientnet-b5 ^
      --fold 0 ^
      --threshold 0.50
"""

import os
import json
import sys
from pathlib import Path
import argparse

import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import torch
import torch.nn.functional as F
from torchvision.transforms import functional as TF

import segmentation_models_pytorch as smp
from tqdm import tqdm
from scipy import ndimage as ndi
import cv2

# Intentar importar módulos locales (si están disponibles)
# Primero intentar agregar rutas comunes al PYTHONPATH
import sys
from pathlib import Path

# Rutas posibles donde pueden estar los módulos
possible_paths = [
    Path(__file__).parent.parent.parent / "Entrenamientos_2026",  # Desde callos-annotation-tool
    Path("D:/PLesion_upch/Fase3_piloto_entrenamientos/Entrenamientos_2026"),  # Ruta absoluta
    Path("D:\\PLesion_upch\\Fase3_piloto_entrenamientos\\Entrenamientos_2026"),  # Ruta absoluta (Windows)
]

# Agregar rutas al PYTHONPATH
for path in possible_paths:
    path_resolved = path.resolve() if path.exists() else None
    if path_resolved and str(path_resolved) not in sys.path:
        sys.path.insert(0, str(path_resolved))
        print(f"[INFO] Agregado al PYTHONPATH: {path_resolved}")

try:
    from configs.lesion_configs import get_config
    from src.models.builder import build_model
    from src.utils.misc import safe_name
    HAS_LOCAL_MODULES = True
    print(f"[OK] Módulos locales cargados correctamente")
except ImportError as e:
    print(f"[WARN] No se encontraron módulos locales (configs, src).")
    print(f"[WARN] Error: {e}")
    print(f"[WARN] Rutas buscadas: {[str(p) for p in possible_paths]}")
    print(f"[WARN] PYTHONPATH actual (primeras 5): {sys.path[:5]}")
    HAS_LOCAL_MODULES = False


# =====================================================
# UTILIDADES
# =====================================================

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def get_gaussian_weight_map(size, device):
    """Crea un kernel gaussiano para suavizar la unión de parches."""
    sigma = size / 8
    ax = torch.arange(size, device=device) - (size - 1) / 2.
    xx, yy = torch.meshgrid(ax, ax, indexing='ij')
    kernel = torch.exp(-0.5 * (torch.square(xx) + torch.square(yy)) / torch.square(torch.tensor(sigma)))
    return kernel / kernel.max()


def predict_sliding_window(model, image_tensor, window_size, overlap=0.5, device='cuda'):
    """Inferencia con Ventana Deslizante (igual que en predict.py)."""
    _, c, h_orig, w_orig = image_tensor.shape
    h, w = h_orig, w_orig

    pad_h = max(0, window_size - h)
    pad_w = max(0, window_size - w)

    if pad_h > 0 or pad_w > 0:
        image_tensor = torch.nn.functional.pad(image_tensor, (0, pad_w, 0, pad_h), mode='reflect')
        _, _, h, w = image_tensor.shape 

    stride = int(window_size * (1 - overlap))
    
    prob_map = torch.zeros((1, 1, h, w), device=device)
    weight_map = torch.zeros((1, 1, h, w), device=device)
    patch_weight = get_gaussian_weight_map(window_size, device).view(1, 1, window_size, window_size)

    rows = list(range(0, h - window_size + 1, stride))
    cols = list(range(0, w - window_size + 1, stride))
    
    if len(rows) == 0 or rows[-1] + window_size < h: rows.append(h - window_size)
    if len(cols) == 0 or cols[-1] + window_size < w: cols.append(w - window_size)

    model.eval()
    with torch.no_grad():
        with torch.cuda.amp.autocast():
            for y in rows:
                for x in cols:
                    img_patch = image_tensor[:, :, y:y+window_size, x:x+window_size]
                    
                    # TTA Lite (Test Time Augmentation)
                    pred_1 = torch.sigmoid(model(img_patch))
                    pred_h = torch.flip(torch.sigmoid(model(torch.flip(img_patch, [3]))), [3])
                    pred_v = torch.flip(torch.sigmoid(model(torch.flip(img_patch, [2]))), [2])
                    
                    pred_avg = (pred_1 + pred_h + pred_v) / 3.0
                    
                    prob_map[:, :, y:y+window_size, x:x+window_size] += pred_avg * patch_weight
                    weight_map[:, :, y:y+window_size, x:x+window_size] += patch_weight

    final_prob = prob_map / (weight_map + 1e-7)
    
    if pad_h > 0 or pad_w > 0:
        final_prob = final_prob[:, :, :h_orig, :w_orig]

    return final_prob


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def run_export(args):
    """Ejecuta la exportación de predicciones para la web."""
    
    if not HAS_LOCAL_MODULES:
        print("[ERROR] Se requieren los módulos locales (configs, src).")
        print("[ERROR] Asegúrate de ejecutar desde el directorio correcto.")
        sys.exit(1)
    
    # Configuración
    lesion_conf = get_config(args.lesion)
    input_size = lesion_conf["input_size"]
    strategy = lesion_conf["strategy"]
    
    if strategy != "crop":
        print(f"[WARN] Estrategia '{strategy}' detectada. Este script está optimizado para 'crop' (sliding window).")
    
    print(f"\n[CONFIG] Lesión: {args.lesion.upper()}")
    print(f"[CONFIG] Estrategia: {strategy.upper()} (Size: {input_size})")
    print(f"[CONFIG] Arquitectura: {args.arch}, Encoder: {args.encoder}")

    root_path = Path(args.consensus_root)
    lesion_dir = root_path / args.lesion
    
    # Intentar diferentes nombres de CSV
    possible_csvs = [
        lesion_dir / "splits" / f"splits_{args.scenario}.csv",  # splits_all_weeks.csv
        lesion_dir / "splits" / f"kfold_{args.scenario}.csv",   # kfold_all_weeks.csv (fallback)
    ]
    
    kfold_csv = None
    for csv_path in possible_csvs:
        if csv_path.exists():
            kfold_csv = csv_path
            break
    
    if not kfold_csv:
        raise FileNotFoundError(f"No se encontró el CSV de splits. Buscado en: {[str(p) for p in possible_csvs]}")
    
    print(f"[INFO] Usando CSV: {kfold_csv}")
    
    exp_name = f"{safe_name(args.arch)}__{safe_name(args.encoder)}"
    base_output_dir = Path(args.out_root) / args.lesion / args.scenario / exp_name
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Dispositivo: {device}")
    
    # Cargar CSV de splits
    import pandas as pd
    
    # Intentar leer con diferentes encodings
    try:
        df = pd.read_csv(kfold_csv, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(kfold_csv, encoding='latin-1')
        except:
            df = pd.read_csv(kfold_csv, encoding='cp1252')
    
    print(f"[INFO] Total de registros en CSV: {len(df)}")
    print(f"[INFO] Columnas disponibles: {', '.join(df.columns.tolist())}")
    
    # Filtrar solo imágenes de TEST si existe la columna 'split'
    if "split" in df.columns:
        test_df = df[df["split"].str.lower() == "test"]
        print(f"[INFO] Imágenes marcadas como TEST: {len(test_df)}")
        
        if len(test_df) == 0:
            print(f"[WARN] No se encontraron imágenes de test en el CSV.")
            print(f"[WARN] Usando todas las imágenes del CSV...")
            test_df = df
        else:
            df = test_df
            print(f"[OK] Filtrando solo imágenes de TEST")
    else:
        print(f"[WARN] No se encontró columna 'split' en el CSV.")
        print(f"[WARN] Usando todas las imágenes del CSV...")
    
    # Determinar folds a usar (si existe la columna fold)
    if "fold" in df.columns:
        if args.fold == -1:
            active_folds = sorted(df["fold"].unique())
            print(f"[INFO] Modo Ensemble. Folds: {active_folds}")
            # Para ensemble, procesamos todas las imágenes de test
        else:
            active_folds = [args.fold]
            print(f"[INFO] Fold único: {args.fold}")
            # Filtrar solo imágenes del fold específico
            df = df[df["fold"] == args.fold]
    else:
        print(f"[INFO] No se encontró columna 'fold' en el CSV. Procesando todas las imágenes de test.")
        active_folds = []
    
    # Cargar modelos (solo si hay folds)
    models = []
    thresholds = []
    
    if active_folds:
        print("\n[INFO] Cargando modelos...")
        for f_idx in active_folds:
            fold_dir = base_output_dir / f"fold_{f_idx}"
            ckpt_path = fold_dir / "checkpoints" / "best_model.pth"
            json_path = fold_dir / "optimal_threshold.json"
            
            if not ckpt_path.exists():
                print(f"   [WARN] Checkpoint no encontrado en fold {f_idx}: {ckpt_path}")
                continue
            
            model = build_model(args.arch, args.encoder, args.encoder_weights, classes=1)
            state = torch.load(ckpt_path, map_location=device)
            
            # Intentar diferentes formas de cargar el estado
            if isinstance(state, dict):
                if "model_state_dict" in state:
                    model.load_state_dict(state["model_state_dict"], strict=False)
                elif "state_dict" in state:
                    model.load_state_dict(state["state_dict"], strict=False)
                else:
                    model.load_state_dict(state, strict=False)
            else:
                model.load_state_dict(state, strict=False)
            
            model.to(device)
            model.eval()
            models.append(model)
            print(f"   [OK] Fold {f_idx} cargado")
            
            if json_path.exists():
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    thresholds.append(data.get('best_threshold', args.threshold))
            else:
                thresholds.append(args.threshold)
    
    if not models:
        if active_folds:
            raise ValueError("No se encontraron modelos válidos.")
        else:
            # Si no hay folds, necesitamos al menos un modelo
            # Intentar cargar desde el directorio base
            print("\n[INFO] No hay folds en el CSV. Intentando cargar modelo único...")
            base_model_dir = base_output_dir / "fold_0" / "checkpoints" / "best_model.pth"
            if base_model_dir.exists():
                model = build_model(args.arch, args.encoder, args.encoder_weights, classes=1)
                state = torch.load(base_model_dir, map_location=device)
                if isinstance(state, dict):
                    if "model_state_dict" in state:
                        model.load_state_dict(state["model_state_dict"], strict=False)
                    elif "state_dict" in state:
                        model.load_state_dict(state["state_dict"], strict=False)
                    else:
                        model.load_state_dict(state, strict=False)
                else:
                    model.load_state_dict(state, strict=False)
                model.to(device)
                model.eval()
                models.append(model)
                thresholds.append(args.threshold)
                print(f"   [OK] Modelo único cargado")
            else:
                raise ValueError(f"No se encontraron modelos. Buscado en: {base_model_dir}")
    
    final_threshold = sum(thresholds) / len(thresholds) if thresholds else args.threshold
    print(f"[CONFIG] Umbral promedio: {final_threshold:.4f}")
    
    # Preprocessing params
    params = smp.encoders.get_preprocessing_params(args.encoder)
    mean = torch.tensor(params["mean"]).view(1, 3, 1, 1).to(device)
    std = torch.tensor(params["std"]).view(1, 3, 1, 1).to(device)
    
    # Preparar carpetas de salida
    web_dir = Path(args.web_dir)
    web_images_dir = web_dir / "images"
    web_images_dir.mkdir(parents=True, exist_ok=True)
    
    # Procesar imágenes
    cases = []
    
    print(f"\n[INFO] Procesando {len(df)} imágenes...")
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="[INFERENCIA]"):
        stem_name = row["stem"]
        
        # Buscar imagen (usar image_filename del CSV si está disponible, sino buscar por stem)
        img_path = None
        
        if "image_filename" in row and pd.notna(row["image_filename"]):
            # Usar el nombre de archivo del CSV
            img_filename = row["image_filename"]
            img_path = lesion_dir / "images_clean" / img_filename
            if not img_path.exists():
                img_path = lesion_dir / "images" / img_filename
        else:
            # Fallback: buscar por stem (prioridad: images_clean > images)
            for ext in [".jpg", ".jpeg", ".png"]:
                p = lesion_dir / "images_clean" / f"{stem_name}{ext}"
                if p.exists():
                    img_path = p
                    break
            
            if img_path is None:
                for ext in [".jpg", ".jpeg", ".png"]:
                    p = lesion_dir / "images" / f"{stem_name}{ext}"
                    if p.exists():
                        img_path = p
                        break
        
        if not img_path or not img_path.exists():
            print(f"   [WARN] Imagen no encontrada: {stem_name}")
            continue
        
        # Cargar imagen
        img_pil = Image.open(img_path).convert("RGB")
        w_orig, h_orig = img_pil.size
        
        # Preprocesar
        img_t = TF.to_tensor(img_pil).unsqueeze(0).to(device)
        img_t = (img_t - mean) / std
        
        # Inferencia con ensemble
        accum_prob = torch.zeros((1, 1, h_orig, w_orig), device=device)
        
        for m in models:
            prob = predict_sliding_window(m, img_t, input_size, overlap=0.5, device=device)
            accum_prob += prob
        
        avg_prob = accum_prob / len(models)
        
        # Binarizar
        pred_mask = (avg_prob > final_threshold).float().cpu().numpy()[0, 0]
        
        # Filtrar componentes pequeñas (opcional)
        if args.min_area > 0:
            lbl, num = ndi.label(pred_mask.astype(np.uint8), structure=np.ones((3, 3), np.uint8))
            if num > 0:
                cnt = np.bincount(lbl.ravel())
                keep = np.zeros_like(cnt, dtype=bool)
                keep[0] = False
                keep[np.where(cnt >= args.min_area)[0]] = True
                pred_mask = keep[lbl].astype(np.float32)
        
        # Guardar imagen procesada (usar la imagen original, no la procesada)
        # Convertir de tensor normalizado a numpy uint8
        img_denorm = img_t * std + mean
        img_denorm = torch.clamp(img_denorm, 0, 1)
        img_arr = (img_denorm[0].cpu().numpy().transpose(1, 2, 0) * 255).astype(np.uint8)
        img_pil_save = Image.fromarray(img_arr)
        
        out_img_path = web_images_dir / f"{stem_name}.png"
        img_pil_save.save(out_img_path)
        
        # Extraer polígonos
        contours, _ = cv2.findContours(
            (pred_mask * 255).astype(np.uint8),
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
            "case_id": stem_name,
            "image_url": f"images/{stem_name}.png",
            "lesions": lesions
        })
    
    # Guardar data.js
    data_js_path = web_dir / args.data_js_name
    with open(data_js_path, "w", encoding="utf-8") as f:
        f.write("const DATA = ")
        json.dump(cases, f, indent=2)
        f.write(";")
    
    print(f"\n[OK] Exportación completada:")
    print(f"     - {len(cases)} casos procesados")
    print(f"     - Imágenes guardadas en: {web_images_dir}")
    print(f"     - data.js guardado en: {data_js_path}")
    print(f"     - Total de lesiones detectadas: {sum(len(c['lesions']) for c in cases)}")


def parse_args():
    ap = argparse.ArgumentParser(description="Exportar predicciones con folds para herramienta web")
    ap.add_argument("--lesion", type=str, required=True, help="Tipo de lesión (ej: callos)")
    ap.add_argument("--scenario", type=str, required=True, help="Escenario (ej: all_weeks)")
    ap.add_argument("--consensus-root", type=str, required=True, help="Raíz del dataset de consenso")
    ap.add_argument("--out-root", type=str, required=True, help="Raíz de outputs de entrenamiento")
    ap.add_argument("--web-dir", type=str, default="web", help="Directorio de salida para web")
    ap.add_argument("--arch", type=str, default="UnetPlusPlus", help="Arquitectura del modelo")
    ap.add_argument("--encoder", type=str, default="timm-efficientnet-b5", help="Encoder")
    ap.add_argument("--encoder-weights", type=str, default="noisy-student", help="Encoder weights")
    ap.add_argument("--fold", type=int, default=-1, help="Fold a usar (-1 = ensemble todos los folds)")
    ap.add_argument("--threshold", type=float, default=0.50, help="Umbral de binarización")
    ap.add_argument("--min-area", type=int, default=0, help="Área mínima de píxeles para filtrar")
    ap.add_argument("--data-js-name", type=str, default="data.js", help="Nombre del archivo data.js")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_export(args)
