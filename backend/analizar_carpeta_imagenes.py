#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para analizar una carpeta de imágenes y detectar duplicados.
"""

from pathlib import Path
import argparse
from collections import Counter
import hashlib

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def get_file_hash(filepath):
    """Calcula el hash MD5 de un archivo."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def analyze_folder(folder_path):
    """Analiza una carpeta de imágenes."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"[ERROR] La carpeta no existe: {folder_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"ANALISIS DE CARPETA: {folder_path}")
    print(f"{'='*70}\n")
    
    # Listar todas las imágenes
    all_images = []
    for ext in IMG_EXTS:
        all_images.extend(list(folder.glob(f"*{ext}")))
        all_images.extend(list(folder.glob(f"*{ext.upper()}")))
    
    all_images = sorted(all_images)
    total_count = len(all_images)
    
    print(f"[TOTAL DE IMAGENES]")
    print(f"  Total de archivos de imagen encontrados: {total_count}")
    
    # Contar por extensión
    ext_counts = Counter([img.suffix.lower() for img in all_images])
    print(f"\n  Por extension:")
    for ext, count in sorted(ext_counts.items()):
        print(f"    {ext}: {count}")
    
    # Verificar nombres duplicados (mismo nombre, diferente extensión)
    print(f"\n[NOMBRES DE ARCHIVOS]")
    name_counts = Counter([img.stem for img in all_images])
    duplicates_by_name = {name: count for name, count in name_counts.items() if count > 1}
    
    if duplicates_by_name:
        print(f"  Archivos con el mismo nombre (diferente extension): {len(duplicates_by_name)}")
        print(f"  Ejemplos (primeros 10):")
        for name, count in list(duplicates_by_name.items())[:10]:
            matching = [img.name for img in all_images if img.stem == name]
            print(f"    '{name}': {count} archivos -> {', '.join(matching)}")
        if len(duplicates_by_name) > 10:
            print(f"    ... y {len(duplicates_by_name) - 10} mas")
    else:
        print(f"  No hay archivos con el mismo nombre (diferente extension)")
    
    # Verificar duplicados por contenido (hash MD5)
    print(f"\n[DUPLICADOS POR CONTENIDO]")
    print(f"  Calculando hashes MD5 (esto puede tardar)...")
    
    file_hashes = {}
    hash_to_files = {}
    
    for img_path in all_images:
        try:
            file_hash = get_file_hash(img_path)
            file_hashes[img_path] = file_hash
            
            if file_hash not in hash_to_files:
                hash_to_files[file_hash] = []
            hash_to_files[file_hash].append(img_path)
        except Exception as e:
            print(f"    [ERROR] No se pudo leer {img_path.name}: {e}")
    
    # Encontrar duplicados
    duplicates_by_content = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    
    if duplicates_by_content:
        total_duplicate_files = sum(len(files) - 1 for files in duplicates_by_content.values())
        print(f"  Archivos duplicados encontrados: {len(duplicates_by_content)} grupos")
        print(f"  Total de archivos duplicados (que se pueden eliminar): {total_duplicate_files}")
        print(f"\n  Ejemplos de duplicados (primeros 5 grupos):")
        
        for i, (file_hash, files) in enumerate(list(duplicates_by_content.items())[:5]):
            print(f"\n    Grupo {i+1} (hash: {file_hash[:16]}...):")
            for f in files:
                size = f.stat().st_size / 1024  # KB
                print(f"      - {f.name} ({size:.1f} KB)")
        
        if len(duplicates_by_content) > 5:
            print(f"\n    ... y {len(duplicates_by_content) - 5} grupos mas")
    else:
        print(f"  No hay archivos duplicados por contenido")
    
    # Resumen final
    print(f"\n{'='*70}")
    print(f"RESUMEN")
    print(f"{'='*70}")
    print(f"  Total de imagenes: {total_count}")
    print(f"  Nombres unicos: {len(name_counts)}")
    print(f"  Nombres duplicados (diferente extension): {len(duplicates_by_name)}")
    print(f"  Archivos duplicados por contenido: {len(duplicates_by_content)} grupos")
    if duplicates_by_content:
        total_dup = sum(len(files) - 1 for files in duplicates_by_content.values())
        print(f"  Total de archivos que se pueden eliminar: {total_dup}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analizar carpeta de imagenes y detectar duplicados")
    parser.add_argument("folder", type=str, help="Ruta a la carpeta de imagenes")
    
    args = parser.parse_args()
    analyze_folder(args.folder)
