#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para subir imágenes a Firebase Storage
Requiere: pip install firebase-admin
"""
import os
import argparse
from pathlib import Path
from firebase_admin import credentials, initialize_app, storage
import json

def upload_images_to_firebase(images_dir, firebase_config_path, storage_bucket=None):
    """
    Sube todas las imágenes de una carpeta a Firebase Storage.
    
    Args:
        images_dir: Ruta a la carpeta con imágenes (ej: web/images/)
        firebase_config_path: Ruta al archivo JSON de credenciales de Firebase
        storage_bucket: Nombre del bucket (opcional, se puede obtener del config)
    """
    # Cargar credenciales
    if not os.path.exists(firebase_config_path):
        print(f"[ERROR] No se encontró el archivo de credenciales: {firebase_config_path}")
        print("\nPara obtener las credenciales:")
        print("1. Ve a Firebase Console → Project Settings → Service Accounts")
        print("2. Click en 'Generate new private key'")
        print("3. Guarda el archivo JSON como 'firebase-credentials.json'")
        return
    
    cred = credentials.Certificate(firebase_config_path)
    
    # Inicializar Firebase
    if storage_bucket:
        initialize_app(cred, {'storageBucket': storage_bucket})
    else:
        # Intentar obtener el bucket del archivo de credenciales
        with open(firebase_config_path, 'r') as f:
            config = json.load(f)
            bucket_name = config.get('project_id') + '.appspot.com'
        initialize_app(cred, {'storageBucket': bucket_name})
    
    bucket = storage.bucket()
    images_path = Path(images_dir)
    
    if not images_path.exists():
        print(f"[ERROR] No se encontró la carpeta: {images_dir}")
        return
    
    # Obtener todas las imágenes PNG
    image_files = list(images_path.glob("*.png"))
    total = len(image_files)
    
    if total == 0:
        print(f"[ERROR] No se encontraron imágenes PNG en: {images_dir}")
        return
    
    print(f"[INFO] Encontradas {total} imágenes")
    print(f"[INFO] Subiendo a Firebase Storage...")
    
    uploaded = 0
    failed = 0
    
    for idx, img_path in enumerate(image_files, 1):
        try:
            # Nombre del archivo en Storage (usar la carpeta "Revision_de_callos" sin espacios)
            # Firebase Storage Rules no acepta espacios en nombres de carpetas
            blob_name = f"Revision_de_callos/{img_path.name}"
            blob = bucket.blob(blob_name)
            
            # Subir archivo
            blob.upload_from_filename(str(img_path))
            
            # Hacer público (para que se pueda acceder sin autenticación)
            blob.make_public()
            
            uploaded += 1
            if idx % 50 == 0:
                print(f"[PROGRESO] {idx}/{total} imágenes subidas...")
                
        except Exception as e:
            print(f"[ERROR] Error al subir {img_path.name}: {e}")
            failed += 1
    
    print(f"\n[COMPLETADO]")
    print(f"  Subidas: {uploaded}")
    print(f"  Fallidas: {failed}")
    print(f"\n[INFO] Las imágenes están disponibles en:")
    print(f"  https://storage.googleapis.com/{bucket.name}/Revision_de_callos/[nombre_imagen].png")
    print(f"\n[INFO] Ejemplo de URL:")
    if uploaded > 0:
        example_name = image_files[0].name
        print(f"  https://storage.googleapis.com/{bucket.name}/Revision_de_callos/{example_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subir imágenes a Firebase Storage")
    parser.add_argument("--images-dir", required=True, help="Carpeta con imágenes (ej: web/images/)")
    parser.add_argument("--firebase-credentials", required=True, 
                       help="Ruta al archivo JSON de credenciales de Firebase")
    parser.add_argument("--storage-bucket", type=str, default=None,
                       help="Nombre del bucket (opcional, se obtiene del config)")
    
    args = parser.parse_args()
    
    upload_images_to_firebase(
        args.images_dir,
        args.firebase_credentials,
        args.storage_bucket
    )
