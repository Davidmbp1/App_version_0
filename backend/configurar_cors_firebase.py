#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para configurar CORS en Firebase Storage
Requiere: pip install firebase-admin google-cloud-storage
"""
import json
import argparse
from pathlib import Path
from google.cloud import storage
from firebase_admin import credentials, initialize_app

def configure_cors(firebase_config_path, storage_bucket=None):
    """
    Configura CORS en Firebase Storage para permitir acceso desde cualquier origen.
    
    Args:
        firebase_config_path: Ruta al archivo JSON de credenciales de Firebase
        storage_bucket: Nombre del bucket (opcional, se puede obtener del config)
    """
    # Cargar credenciales
    if not Path(firebase_config_path).exists():
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
    
    # Configurar CORS
    cors_config = [
        {
            "origin": ["*"],  # Permitir desde cualquier origen
            "method": ["GET", "HEAD"],  # Solo lectura
            "responseHeader": [
                "Content-Type",
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Methods"
            ],
            "maxAgeSeconds": 3600
        }
    ]
    
    try:
        client = storage.Client.from_service_account_json(firebase_config_path)
        bucket = client.bucket(bucket_name)
        bucket.cors = cors_config
        bucket.patch()
        
        print(f"[OK] CORS configurado exitosamente para el bucket: {bucket_name}")
        print(f"\n[INFO] Configuracion CORS aplicada:")
        print(f"  - Origenes permitidos: * (todos)")
        print(f"  - Metodos: GET, HEAD")
        print(f"  - Headers: Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Methods")
        
    except Exception as e:
        print(f"[ERROR] Error al configurar CORS: {e}")
        print(f"\n[INFO] Alternativa: Configura CORS manualmente desde Google Cloud Console:")
        print(f"  1. Ve a: https://console.cloud.google.com/storage/browser/{bucket_name}")
        print(f"  2. Haz clic en 'Permissions' -> 'CORS configuration'")
        print(f"  3. Agrega la configuracion CORS")
        print(f"\n[INFO] Configuracion CORS a agregar:")
        print(json.dumps(cors_config, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configurar CORS en Firebase Storage")
    parser.add_argument("--firebase-credentials", required=True, 
                       help="Ruta al archivo JSON de credenciales de Firebase")
    parser.add_argument("--storage-bucket", type=str, default=None,
                       help="Nombre del bucket (opcional, se obtiene del config)")
    
    args = parser.parse_args()
    
    configure_cors(
        args.firebase_credentials,
        args.storage_bucket
    )
