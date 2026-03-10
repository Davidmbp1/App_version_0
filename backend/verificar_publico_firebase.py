#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar y hacer público un archivo en Firebase Storage
Requiere: pip install firebase-admin
"""
import os
import argparse
from pathlib import Path
from firebase_admin import credentials, initialize_app, storage
import json

def verificar_y_publicar_archivo(firebase_config_path, blob_name, storage_bucket=None):
    """
    Verifica si un archivo está público y lo hace público si no lo está.
    
    Args:
        firebase_config_path: Ruta al archivo JSON de credenciales de Firebase
        blob_name: Nombre del archivo en Storage (ej: "Revision_de_callos/data.js")
        storage_bucket: Nombre del bucket (opcional, se puede obtener del config)
    """
    # Cargar credenciales
    if not os.path.exists(firebase_config_path):
        print(f"[ERROR] No se encontró el archivo de credenciales: {firebase_config_path}")
        return
    
    cred = credentials.Certificate(firebase_config_path)
    
    # Inicializar Firebase
    if storage_bucket:
        initialize_app(cred, {'storageBucket': storage_bucket})
        bucket_name = storage_bucket
    else:
        with open(firebase_config_path, 'r') as f:
            config = json.load(f)
            bucket_name = config.get('project_id') + '.appspot.com'
        initialize_app(cred, {'storageBucket': bucket_name})
    
    bucket = storage.bucket()
    blob = bucket.blob(blob_name)
    
    if not blob.exists():
        print(f"[ERROR] El archivo no existe: {blob_name}")
        return
    
    # Verificar si es público
    try:
        blob.reload()
        is_public = blob.public_url is not None
        
        if not is_public:
            print(f"[INFO] El archivo no es público. Haciéndolo público...")
            blob.make_public()
            print(f"[OK] Archivo hecho público exitosamente")
        else:
            print(f"[OK] El archivo ya es público")
        
        # Obtener URL pública
        blob.reload()
        public_url = blob.public_url
        print(f"\n[INFO] URL pública del archivo:")
        print(f"  {public_url}")
        
        # Verificar permisos
        acl = blob.acl
        print(f"\n[INFO] Permisos ACL:")
        for entry in acl.get_entities():
            print(f"  - {entry}")
        
    except Exception as e:
        print(f"[ERROR] Error al verificar/hacer público el archivo: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verificar y hacer público un archivo en Firebase Storage")
    parser.add_argument("--firebase-credentials", required=True, 
                       help="Ruta al archivo JSON de credenciales de Firebase")
    parser.add_argument("--blob-name", required=True,
                       help="Nombre del archivo en Storage (ej: Revision_de_callos/data.js)")
    parser.add_argument("--storage-bucket", type=str, default=None,
                       help="Nombre del bucket (opcional, se obtiene del config)")
    
    args = parser.parse_args()
    
    verificar_y_publicar_archivo(
        args.firebase_credentials,
        args.blob_name,
        args.storage_bucket
    )
