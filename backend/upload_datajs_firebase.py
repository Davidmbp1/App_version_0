#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para subir data.js a Firebase Storage
Requiere: pip install firebase-admin
"""
import os
import argparse
from pathlib import Path
from firebase_admin import credentials, initialize_app, storage
import json

def upload_datajs_to_firebase(datajs_path, firebase_config_path, storage_bucket=None):
    """
    Sube data.js a Firebase Storage.
    
    Args:
        datajs_path: Ruta al archivo data.js
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
    datajs_file = Path(datajs_path)
    
    if not datajs_file.exists():
        print(f"[ERROR] No se encontró el archivo: {datajs_path}")
        return
    
    file_size_mb = datajs_file.stat().st_size / (1024 * 1024)
    print(f"[INFO] Archivo encontrado: {datajs_file.name} ({file_size_mb:.2f} MB)")
    
    try:
        # Nombre del archivo en Storage (usar la carpeta "Revision_de_callos")
        blob_name = f"Revision_de_callos/data.js"
        blob = bucket.blob(blob_name)
        
        # Subir archivo
        print(f"[INFO] Subiendo data.js a Firebase Storage...")
        blob.upload_from_filename(str(datajs_file))
        
        # Hacer público (para que se pueda acceder sin autenticación)
        blob.make_public()
        
        print(f"\n[COMPLETADO] data.js subido exitosamente")
        print(f"\n[INFO] URL de acceso:")
        print(f"  https://storage.googleapis.com/{bucket.name}/Revision_de_callos/data.js")
        
    except Exception as e:
        print(f"[ERROR] Error al subir data.js: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subir data.js a Firebase Storage")
    parser.add_argument("--datajs-path", required=True, help="Ruta al archivo data.js (ej: web/data.js)")
    parser.add_argument("--firebase-credentials", required=True, 
                       help="Ruta al archivo JSON de credenciales de Firebase")
    parser.add_argument("--storage-bucket", type=str, default=None,
                       help="Nombre del bucket (opcional, se obtiene del config)")
    
    args = parser.parse_args()
    
    upload_datajs_to_firebase(
        args.datajs_path,
        args.firebase_credentials,
        args.storage_bucket
    )
