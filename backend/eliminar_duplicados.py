#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para eliminar archivos duplicados en carpetas de imágenes y máscaras.
Elimina duplicados basándose en el hash MD5 del contenido.
"""

from pathlib import Path
import argparse
import hashlib
from collections import defaultdict
import sys

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def get_file_hash(filepath):
    """Calcula el hash MD5 de un archivo."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"    [ERROR] No se pudo leer {filepath.name}: {e}")
        return None


def find_duplicates(folder_path, dry_run=True):
    """Encuentra duplicados en una carpeta."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"  [WARN] La carpeta no existe: {folder_path}")
        return [], []
    
    # Listar todas las imágenes
    all_files = []
    for ext in IMG_EXTS:
        all_files.extend(list(folder.glob(f"*{ext}")))
        all_files.extend(list(folder.glob(f"*{ext.upper()}")))
    
    if not all_files:
        return [], []
    
    print(f"  Analizando {len(all_files)} archivos...")
    
    # Calcular hashes
    hash_to_files = defaultdict(list)
    
    for file_path in all_files:
        file_hash = get_file_hash(file_path)
        if file_hash:
            hash_to_files[file_hash].append(file_path)
    
    # Encontrar duplicados (grupos con más de 1 archivo)
    duplicates = []
    files_to_keep = []
    
    for file_hash, files in hash_to_files.items():
        if len(files) > 1:
            # Ordenar por nombre para mantener consistencia
            files_sorted = sorted(files)
            # Mantener el primero, eliminar el resto
            files_to_keep.append(files_sorted[0])
            duplicates.extend(files_sorted[1:])
    
    return files_to_keep, duplicates


def process_folder(folder_path, dry_run=True):
    """Procesa una carpeta y elimina duplicados."""
    folder = Path(folder_path)
    
    print(f"\n{'='*70}")
    print(f"CARPETA: {folder_path}")
    print(f"{'='*70}")
    
    if not folder.exists():
        print(f"  [ERROR] La carpeta no existe")
        return 0, 0
    
    files_to_keep, duplicates = find_duplicates(folder_path, dry_run)
    
    if not duplicates:
        print(f"  No se encontraron duplicados")
        return 0, 0
    
    print(f"\n  Duplicados encontrados: {len(duplicates)} archivos")
    print(f"  Archivos que se mantendran: {len(files_to_keep)}")
    
    # Mostrar algunos ejemplos
    if len(duplicates) > 0:
        print(f"\n  Ejemplos de archivos a eliminar (primeros 5):")
        for dup in duplicates[:5]:
            size = dup.stat().st_size / 1024  # KB
            print(f"    - {dup.name} ({size:.1f} KB)")
        if len(duplicates) > 5:
            print(f"    ... y {len(duplicates) - 5} mas")
    
    # Eliminar duplicados
    deleted_count = 0
    deleted_size = 0
    
    if not dry_run:
        print(f"\n  Eliminando duplicados...")
        for dup_file in duplicates:
            try:
                size = dup_file.stat().st_size
                dup_file.unlink()
                deleted_count += 1
                deleted_size += size
            except Exception as e:
                print(f"    [ERROR] No se pudo eliminar {dup_file.name}: {e}")
        
        print(f"  [OK] Eliminados {deleted_count} archivos ({deleted_size / 1024 / 1024:.1f} MB)")
    else:
        print(f"\n  [DRY RUN] No se eliminaron archivos (modo vista previa)")
        deleted_size = sum(f.stat().st_size for f in duplicates)
        print(f"  Se eliminarian {len(duplicates)} archivos ({deleted_size / 1024 / 1024:.1f} MB)")
    
    return len(duplicates), deleted_size


def main():
    parser = argparse.ArgumentParser(description="Eliminar archivos duplicados en carpetas de imagenes y mascaras")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Modo vista previa (no elimina archivos)")
    parser.add_argument("--base-dir", type=str, 
                       default="D:\\PrevencionLesion-UPCH-Monitoreo\\entrenamientos_2026\\consensus_dataset_majority",
                       help="Directorio base del dataset")
    
    args = parser.parse_args()
    
    base_dir = Path(args.base_dir)
    
    # Definir carpetas a procesar
    lesions = ["callos", "callo_hemorragico", "decoloracion", "eritema", "fisura", "ulcera"]
    subfolders = ["images", "masks"]
    
    print(f"\n{'='*70}")
    print(f"ELIMINACION DE DUPLICADOS")
    print(f"{'='*70}")
    print(f"Directorio base: {base_dir}")
    print(f"Modo: {'VISTA PREVIA (dry-run)' if args.dry_run else 'ELIMINACION REAL'}")
    print(f"{'='*70}")
    
    if not args.dry_run:
        respuesta = input("\n¿Estas seguro de que quieres eliminar los duplicados? (escribe 'SI' para continuar): ")
        if respuesta != "SI":
            print("Operacion cancelada.")
            return
    
    total_deleted = 0
    total_size = 0
    
    # Procesar cada lesión
    for lesion in lesions:
        lesion_dir = base_dir / lesion
        
        if not lesion_dir.exists():
            print(f"\n[SKIP] Lesion '{lesion}' no existe en {lesion_dir}")
            continue
        
        print(f"\n\n{'#'*70}")
        print(f"LESION: {lesion.upper()}")
        print(f"{'#'*70}")
        
        # Procesar images y masks
        for subfolder in subfolders:
            folder_path = lesion_dir / subfolder
            if folder_path.exists():
                deleted, size = process_folder(folder_path, dry_run=args.dry_run)
                total_deleted += deleted
                total_size += size
            else:
                print(f"\n[SKIP] Carpeta no existe: {folder_path}")
    
    # Resumen final
    print(f"\n\n{'='*70}")
    print(f"RESUMEN FINAL")
    print(f"{'='*70}")
    if args.dry_run:
        print(f"  Total de archivos que se eliminarian: {total_deleted}")
        print(f"  Espacio que se liberaria: {total_size / 1024 / 1024:.1f} MB")
        print(f"\n  Para eliminar realmente, ejecuta sin --dry-run")
    else:
        print(f"  Total de archivos eliminados: {total_deleted}")
        print(f"  Espacio liberado: {total_size / 1024 / 1024:.1f} MB")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
