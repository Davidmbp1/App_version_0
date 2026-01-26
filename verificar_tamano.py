#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar el tamaño de los archivos antes de subir a GitHub Pages.
"""

from pathlib import Path

def get_size_mb(path):
    """Obtiene el tamaño de un archivo o directorio en MB."""
    if path.is_file():
        return path.stat().st_size / (1024 * 1024)
    elif path.is_dir():
        total = 0
        for item in path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
        return total / (1024 * 1024)
    return 0

def main():
    web_dir = Path("web")
    
    if not web_dir.exists():
        print("[ERROR] No se encontró el directorio 'web'")
        return
    
    print("=" * 60)
    print("Verificación de Tamaño para GitHub Pages")
    print("=" * 60)
    print()
    
    # Verificar imágenes
    images_dir = web_dir / "images"
    images_size = 0
    image_count = 0
    
    if images_dir.exists():
        images_size = get_size_mb(images_dir)
        image_count = len(list(images_dir.glob("*.png"))) + len(list(images_dir.glob("*.jpg"))) + len(list(images_dir.glob("*.jpeg")))
        print(f"Imágenes: {images_size:.2f} MB ({image_count} archivos)")
    else:
        print("Imágenes: No encontrado")
    
    # Verificar data.js
    data_js = web_dir / "data.js"
    data_js_size = 0
    if data_js.exists():
        data_js_size = get_size_mb(data_js)
        print(f"data.js: {data_js_size:.2f} MB")
    else:
        print("data.js: No encontrado")
    
    # Verificar index.html
    index_html = web_dir / "index.html"
    index_size = get_size_mb(index_html) if index_html.exists() else 0
    
    # Total
    total_size = images_size + data_js_size + index_size
    print(f"Total: {total_size:.2f} MB")
    print()
    
    # Verificar límites
    print("=" * 60)
    print("Límites de GitHub Pages:")
    print("  - Repositorio público: 1 GB máximo")
    print("  - Archivo individual: 100 MB máximo")
    print("=" * 60)
    print()
    
    # Recomendaciones
    if total_size < 500:
        print("OK: El tamaño está bien para GitHub Pages")
        print("   Puedes proceder con el despliegue sin problemas.")
    elif total_size < 1000:
        print("ADVERTENCIA: Estás cerca del límite de 1 GB")
        print("   GitHub Pages funcionará, pero considera:")
        print("   - Usar Netlify o Vercel para más espacio")
        print("   - Optimizar imágenes si es posible")
    else:
        print("PROBLEMA: El tamaño excede 1 GB")
        print("   GitHub Pages NO aceptará este repositorio.")
        print("   Opciones:")
        print("   1. Usar Netlify (100 GB/mes gratis, sin límite de almacenamiento)")
        print("   2. Usar Vercel (similar a Netlify)")
        print("   3. Optimizar/redimensionar imágenes")
        print("   4. Usar servidor local o propio")
    
    # Verificar archivos individuales grandes
    print()
    print("Verificando archivos individuales grandes (>50 MB)...")
    large_files = []
    for item in web_dir.rglob('*'):
        if item.is_file():
            size_mb = get_size_mb(item)
            if size_mb > 50:
                large_files.append((item, size_mb))
    
    if large_files:
        print(f"Encontrados {len(large_files)} archivos grandes:")
        for file_path, size_mb in sorted(large_files, key=lambda x: x[1], reverse=True)[:10]:
            rel_path = file_path.relative_to(web_dir)
            print(f"   - {rel_path}: {size_mb:.2f} MB")
        if len(large_files) > 10:
            print(f"   ... y {len(large_files) - 10} más")
    else:
        print("No hay archivos individuales muy grandes")
    
    print()

if __name__ == "__main__":
    main()
