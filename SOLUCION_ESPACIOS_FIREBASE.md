# Solución para el Error de Espacios en Firebase Storage Rules

## ❌ Problema
Firebase Storage Rules **NO acepta espacios** en los nombres de carpetas directamente. Por eso obtienes el error:
```
Line 9: Missing 'match' keyword before path.
Line 9: Unexpected 'de'.
```

## ✅ Solución Recomendada: Renombrar la Carpeta

### Opción 1: Renombrar en Firebase Console (2 minutos)

1. Ve a Firebase Console → **Storage** → **Files**
2. Encuentra la carpeta **"Revision de callos"**
3. Haz clic derecho → **Rename** (o selecciona y usa el menú)
4. Renómbrala a: **`Revision_de_callos`** (sin espacios, usa guiones bajos)
5. **Actualiza el código** para usar el nuevo nombre (ver abajo)

### Opción 2: Crear Nueva Carpeta (si no puedes renombrar)

1. Crea una nueva carpeta en Firebase Storage: **`Revision_de_callos`**
2. Sube las imágenes a esta nueva carpeta
3. **Actualiza el código** para usar el nuevo nombre

## 🔧 Actualizar el Código

Después de renombrar la carpeta, actualiza estos archivos:

### 1. `web/index.html` (línea ~746)
Cambia:
```javascript
return `https://storage.googleapis.com/${FIREBASE_STORAGE_BUCKET}/Revision%20de%20callos/${imageName}`;
```

Por:
```javascript
return `https://storage.googleapis.com/${FIREBASE_STORAGE_BUCKET}/Revision_de_callos/${imageName}`;
```

### 2. `backend/upload_images_firebase.py` (línea ~67)
Cambia:
```python
blob_name = f"Revision de callos/{img_path.name}"
```

Por:
```python
blob_name = f"Revision_de_callos/{img_path.name}"
```

### 3. `REGLAS_FIREBASE_STORAGE.txt`
Usa el contenido de `REGLAS_FIREBASE_STORAGE_ALTERNATIVA.txt` que ya tiene la regla correcta:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /videos_onb_instr/{file} {
      allow read: if true;
    }
    match /Revision_de_callos/{file} {
      allow read: if true;
    }
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 📋 Pasos Completos

1. ✅ Renombrar carpeta en Firebase Console: `Revision de callos` → `Revision_de_callos`
2. ✅ Actualizar `web/index.html` (cambiar URL)
3. ✅ Actualizar `backend/upload_images_firebase.py` (cambiar blob_name)
4. ✅ Actualizar reglas de Storage (usar `REGLAS_FIREBASE_STORAGE_ALTERNATIVA.txt`)
5. ✅ Subir imágenes usando el script (se subirán a la nueva carpeta)

## 🚀 Comandos Rápidos

```powershell
# Después de renombrar la carpeta en Firebase Console
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"

# Actualizar código (yo lo haré automáticamente)
# Luego subir imágenes:
python backend/upload_images_firebase.py --images-dir "web/images" --firebase-credentials "backend/firebase-credentials.json" --storage-bucket "foot-selfie---multiplatform.firebasestorage.app"
```

## ⚠️ Si Ya Subiste Imágenes a "Revision de callos"

Si ya subiste imágenes a la carpeta con espacios:
1. **Opción A**: Renombrar la carpeta en Firebase Console (si es posible)
2. **Opción B**: Crear nueva carpeta `Revision_de_callos` y volver a subir las imágenes
3. **Opción C**: Eliminar la carpeta vieja y crear la nueva
