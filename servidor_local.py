#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Servidor web simple para la herramienta de anotación de callos.

Uso:
    python servidor_local.py

Luego abre en el navegador:
    http://localhost:8000

Para acceder desde otras computadoras en la misma red:
    http://TU_IP_LOCAL:8000
    (ej: http://192.168.1.100:8000)
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Cambiar al directorio web
WEB_DIR = Path(__file__).parent / "web"
if not WEB_DIR.exists():
    print(f"[ERROR] No se encontró el directorio web: {WEB_DIR}")
    sys.exit(1)

os.chdir(WEB_DIR)

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Agregar headers CORS para permitir acceso desde otros orígenes
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # Log más limpio
        print(f"[{self.log_date_time_string()}] {args[0]}")

def get_local_ip():
    """Obtiene la IP local de la máquina."""
    import socket
    try:
        # Conectar a un servidor externo para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == "__main__":
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("Servidor web para Callos Annotation Tool")
    print("=" * 60)
    print(f"\n[INFO] Directorio web: {WEB_DIR.absolute()}")
    print(f"[INFO] Servidor iniciado en:")
    print(f"       - Local:    http://localhost:{PORT}")
    print(f"       - Red:      http://{local_ip}:{PORT}")
    print(f"\n[INFO] Para detener el servidor, presiona Ctrl+C")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Servidor detenido.")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n[ERROR] El puerto {PORT} ya está en uso.")
            print(f"[INFO] Cierra otras aplicaciones que usen el puerto o cambia el puerto en el script.")
        else:
            print(f"\n[ERROR] Error al iniciar el servidor: {e}")
        sys.exit(1)
