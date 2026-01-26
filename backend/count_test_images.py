#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para contar imágenes de test en el dataset.

Muestra:
- Total de imágenes en cada carpeta (images, images_clean, masks)
- Imágenes por fold según el CSV de splits
- Estadísticas del dataset
"""

import csv
from pathlib import Path
import argparse
from collections import Counter

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def count_images_in_dir(directory):
    """Cuenta imágenes en un directorio."""
    if not directory.exists():
        return 0, []
    
    images = []
    for ext in IMG_EXTS:
        images.extend(list(directory.glob(f"*{ext}")))
        images.extend(list(directory.glob(f"*{ext.upper()}")))
    
    return len(images), sorted(images)


def analyze_dataset(consensus_root, lesion, scenario):
    """Analiza el dataset y muestra estadísticas, especialmente imágenes de TEST."""
    root_path = Path(consensus_root)
    lesion_dir = root_path / lesion
    
    print(f"\n{'='*70}")
    print(f"ANÁLISIS DEL DATASET: {lesion.upper()}")
    print(f"{'='*70}")
    print(f"Directorio raíz: {lesion_dir}")
    
    # Contar imágenes en diferentes carpetas
    print(f"\n[IMÁGENES POR CARPETA]")
    print("-" * 70)
    
    images_dir = lesion_dir / "images"
    images_clean_dir = lesion_dir / "images_clean"
    masks_dir = lesion_dir / "masks"
    
    count_img, _ = count_images_in_dir(images_dir)
    count_img_clean, _ = count_images_in_dir(images_clean_dir)
    count_masks, _ = count_images_in_dir(masks_dir)
    
    print(f"  images/          : {count_img:4d} imágenes")
    print(f"  images_clean/    : {count_img_clean:4d} imágenes")
    print(f"  masks/            : {count_masks:4d} máscaras")
    
    # Analizar CSV de splits
    kfold_csv = lesion_dir / "splits" / f"kfold_{scenario}.csv"
    
    if not kfold_csv.exists():
        print(f"\n[WARN] No se encontró el CSV de splits: {kfold_csv}")
        return
    
    print(f"\n[SPLITS K-FOLD]")
    print("-" * 70)
    print(f"CSV: {kfold_csv}")
    
    # Leer CSV usando csv estándar (más robusto)
    rows = []
    headers = []
    try:
        with open(kfold_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if row:  # Ignorar filas vacías
                    rows.append(row)
    except UnicodeDecodeError:
        try:
            with open(kfold_csv, 'r', encoding='latin-1') as f:
                reader = csv.reader(f)
                headers = next(reader)
                for row in reader:
                    if row:
                        rows.append(row)
        except:
            with open(kfold_csv, 'r', encoding='cp1252') as f:
                reader = csv.reader(f)
                headers = next(reader)
                for row in reader:
                    if row:
                        rows.append(row)
    
    # Convertir a diccionarios
    df_data = []
    for row in rows:
        if len(row) == len(headers):
            df_data.append(dict(zip(headers, row)))
    
    print(f"\n  Total de registros en CSV: {len(df_data)}")
    print(f"  Columnas: {', '.join(headers)}")
    
    # Detectar si hay columna de split (train/val/test)
    has_split_col = "split" in headers or "set" in headers
    split_col = "split" if "split" in headers else ("set" if "set" in headers else None)
    
    # Contar por fold
    if "fold" in headers:
        fold_values = [int(row.get("fold", 0)) for row in df_data if row.get("fold", "").isdigit()]
        fold_counts = Counter(fold_values)
        print(f"\n  Distribución por fold:")
        for fold in sorted(fold_counts.keys()):
            print(f"    Fold {fold}: {fold_counts[fold]:4d} imágenes")
        
        print(f"\n  Total de folds únicos: {len(fold_counts)}")
        if fold_counts:
            print(f"  Rango de folds: {min(fold_counts.keys())} - {max(fold_counts.keys())}")
    
    # IDENTIFICAR IMÁGENES DE TEST
    print(f"\n{'='*70}")
    print(f"IMÁGENES DE TEST")
    print(f"{'='*70}")
    
    if has_split_col:
        # Si hay columna de split, filtrar solo test
        test_data = [row for row in df_data if row.get(split_col, "").lower() == "test"]
        print(f"\n  Columna de split detectada: '{split_col}'")
        print(f"  Imágenes marcadas como TEST en CSV: {len(test_data)}")
        
        if len(test_data) > 0:
            print(f"\n  Distribución de TEST por fold:")
            if "fold" in headers:
                test_fold_values = [int(row.get("fold", 0)) for row in test_data if row.get("fold", "").isdigit()]
                test_fold_counts = Counter(test_fold_values)
                for fold in sorted(test_fold_counts.keys()):
                    print(f"    Fold {fold}: {test_fold_counts[fold]:4d} imágenes de test")
        else:
            print(f"  [INFO] No hay imágenes marcadas como 'test' en la columna '{split_col}'")
            print(f"  [INFO] Asumiendo que TODAS las imágenes del CSV son de test (k-fold)")
            test_data = df_data
    else:
        # Si no hay columna de split, asumir que todas son de test
        print(f"\n  No se encontró columna 'split' o 'set' en el CSV")
        print(f"  [ASUMIENDO] Todas las imágenes del CSV son de TEST (k-fold cross-validation)")
        test_data = df_data
    
    # Verificar existencia de imágenes de TEST
    print(f"\n[VERIFICACIÓN DE IMÁGENES DE TEST]")
    print("-" * 70)
    
    missing_test = []
    found_test = []
    found_test_by_folder = {"images_clean": 0, "images": 0}
    
    for row in test_data:
        stem = row.get("stem", "")
        if not stem:
            continue
        
        # Buscar en images_clean primero
        found = False
        for ext in [".jpg", ".jpeg", ".png"]:
            p_clean = images_clean_dir / f"{stem}{ext}"
            p_img = images_dir / f"{stem}{ext}"
            
            if p_clean.exists():
                found_test.append((stem, "images_clean"))
                found_test_by_folder["images_clean"] += 1
                found = True
                break
            elif p_img.exists():
                found_test.append((stem, "images"))
                found_test_by_folder["images"] += 1
                found = True
                break
        
        if not found:
            missing_test.append(stem)
    
    print(f"  Imágenes de TEST encontradas: {len(found_test)}")
    print(f"    - En images_clean/: {found_test_by_folder['images_clean']}")
    print(f"    - En images/: {found_test_by_folder['images']}")
    print(f"  Imágenes de TEST faltantes: {len(missing_test)}")
    
    if missing_test:
        print(f"\n  Primeras 10 imágenes de TEST faltantes:")
        for stem in missing_test[:10]:
            print(f"    - {stem}")
        if len(missing_test) > 10:
            print(f"    ... y {len(missing_test) - 10} más")
    
    # Resumen final
    print(f"\n{'='*70}")
    print(f"RESUMEN FINAL")
    print(f"{'='*70}")
    print(f"  Total de imagenes en carpetas: {max(count_img, count_img_clean)}")
    print(f"  Total de registros en CSV: {len(df_data)}")
    print(f"  IMAGENES DE TEST: {len(test_data)} (en CSV)")
    print(f"  Imagenes de TEST encontradas: {len(found_test)}")
    print(f"  Imagenes de TEST faltantes: {len(missing_test)}")
    
    if "fold" in headers and fold_counts:
        print(f"\n  Folds disponibles: {len(fold_counts)}")
        print(f"  Rango de folds: {min(fold_counts.keys())} - {max(fold_counts.keys())}")
    
    print(f"{'='*70}\n")
    
    # Respuesta directa
    print(f"RESPUESTA: Hay {len(found_test)} imagenes de TEST disponibles para callos\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Contar imágenes de test en el dataset")
    parser.add_argument("--lesion", type=str, required=True, help="Tipo de lesión (ej: callos)")
    parser.add_argument("--scenario", type=str, required=True, help="Escenario (ej: all_weeks)")
    parser.add_argument("--consensus-root", type=str, required=True, help="Raíz del dataset de consenso")
    
    args = parser.parse_args()
    analyze_dataset(args.consensus_root, args.lesion, args.scenario)
