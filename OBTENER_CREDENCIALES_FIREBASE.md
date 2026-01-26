# Cómo Obtener las Credenciales de Firebase

## Pasos Detallados:

## 1. Ir a Firebase Console

1. Abre tu navegador y ve a: https://console.firebase.google.com/
2. Selecciona tu proyecto: **FS-multiplatform**

## 2. Ir a Service Accounts

1. Haz clic en el ícono de **⚙️ Settings** (Configuración) en la parte superior izquierda
2. Selecciona **"Project settings"** (Configuración del proyecto)
3. Ve a la pestaña **"Service accounts"** (Cuentas de servicio)

## 3. Generar Nueva Clave Privada

1. En la sección **"Service accounts"**, verás información sobre tu proyecto
2. Busca el botón **"Generate new private key"** (Generar nueva clave privada)
3. Haz clic en ese botón
4. Aparecerá un popup de advertencia sobre mantener la clave segura
5. Haz clic en **"Generate key"** (Generar clave)

## 4. Descargar el Archivo JSON

1. Se descargará automáticamente un archivo JSON
2. El nombre del archivo será algo como: `foot-selfie---multiplatform-firebase-adminsdk-xxxxx-xxxxxxxxxx.json`
3. **NO lo renombres todavía**

## 5. Guardar el Archivo en el Proyecto

Tienes dos opciones:

### Opción A: Mover el archivo (Recomendado)

1. El archivo se descargó en tu carpeta de **Descargas** (Downloads)
2. Muévelo o cópialo a: `D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool\backend\firebase-credentials.json`
3. **Renómbralo** a: `firebase-credentials.json` (sin el nombre largo)

### Opción B: Usar el archivo con su nombre original

Si prefieres no renombrarlo, puedes usar el comando así:

```powershell
# Reemplaza "nombre-del-archivo.json" con el nombre real del archivo descargado
python backend/upload_images_firebase.py --images-dir "web/images" --firebase-credentials "backend/nombre-del-archivo.json" --storage-bucket "foot-selfie---multiplatform.firebasestorage.app"
```

## 6. Verificar que el Archivo Está en el Lugar Correcto

```powershell
# Verificar que existe
Test-Path "backend/firebase-credentials.json"

# O ver todos los archivos JSON en backend
Get-ChildItem -Path "backend" -Filter "*.json"
```

## 7. Ejecutar el Script de Nuevo

Una vez que el archivo esté en su lugar:

```powershell
python backend/upload_images_firebase.py --images-dir "web/images" --firebase-credentials "backend/firebase-credentials.json" --storage-bucket "foot-selfie---multiplatform.firebasestorage.app"
```

## ⚠️ Importante: Seguridad

- **NO subas este archivo a GitHub** (ya está en `.gitignore`)
- Este archivo contiene credenciales sensibles
- Manténlo solo en tu máquina local
- Si alguien más necesita subir imágenes, debe obtener sus propias credenciales

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo"
- Verifica que el archivo esté en `backend/firebase-credentials.json`
- Verifica que el nombre del archivo sea exacto (sin espacios extra)
- Usa comillas en la ruta si tiene espacios

### Error: "Permission denied"
- Verifica que las reglas de Storage permitan escritura temporalmente
- O sube manualmente desde Firebase Console

### Error: "Invalid credentials"
- Verifica que el archivo JSON no esté corrupto
- Genera una nueva clave privada si es necesario
