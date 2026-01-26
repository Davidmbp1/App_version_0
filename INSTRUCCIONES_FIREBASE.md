# Instrucciones para Usar Firebase Storage

## ✅ Ventajas
- **GitHub queda liviano**: Solo código, no imágenes (~2.8 GB menos)
- **Netlify funciona perfecto**: Solo sirve HTML/JS pequeño
- **No cambias HTML/CSS/JS**: Solo activas una opción
- **Escalable**: Firebase maneja el tráfico de imágenes

## 📋 Pasos Completos

### 1. Crear Proyecto en Firebase (5 minutos)

1. Ve a: https://console.firebase.google.com/
2. Click en **"Add project"** o selecciona uno existente
3. Nombre del proyecto: `callos-annotation-tool` (o el que prefieras)
4. Sigue los pasos (puedes desactivar Google Analytics)

### 2. Habilitar Firebase Storage (2 minutos)

1. En el proyecto, ve a **Storage** (menú izquierdo)
2. Click en **"Get started"**
3. Selecciona **"Start in test mode"**
4. Selecciona ubicación: `us-central1` (o la más cercana a ti)
5. Click **"Done"**

### 3. Configurar Reglas de Storage (2 minutos)

1. Ve a **Storage** → **Rules**
2. Reemplaza las reglas con:
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /images/{imageName} {
      allow read: if true;  // Permite lectura pública (sin autenticación)
      allow write: if false; // Solo tú puedes escribir
    }
  }
}
```
3. Click **"Publish"**

### 4. Obtener Nombre del Bucket (1 minuto)

1. Ve a **Storage** → **Files**
2. En la parte superior verás algo como: `gs://tu-proyecto.appspot.com`
3. El nombre del bucket es: `tu-proyecto.appspot.com`
4. **Copia este nombre** (lo necesitarás en el paso 6)

### 5. Obtener Credenciales para Subir Imágenes (3 minutos)

1. Ve a **Project Settings** (⚙️) → **Service Accounts**
2. Click en **"Generate new private key"**
3. Click **"Generate key"** en el popup
4. Se descargará un archivo JSON (ej: `tu-proyecto-firebase-adminsdk-xxxxx.json`)
5. **Guarda este archivo** en: `backend/firebase-credentials.json`

### 6. Subir Imágenes a Firebase Storage (10-30 minutos dependiendo de tu conexión)

```powershell
# Activar entorno virtual
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"
..\.venv\Scripts\activate

# Instalar Firebase Admin SDK
pip install firebase-admin

# Subir imágenes (reemplaza con tu archivo de credenciales)
python backend/upload_images_firebase.py --images-dir "web/images" --firebase-credentials "backend/firebase-credentials.json"
```

Esto subirá las 962 imágenes. Puede tardar 10-30 minutos dependiendo de tu conexión.

### 7. Activar Firebase Storage en el HTML (1 minuto)

1. Abre `web/index.html`
2. Busca la línea:
   ```javascript
   const USE_FIREBASE_STORAGE = false;
   ```
3. Cámbiala a:
   ```javascript
   const USE_FIREBASE_STORAGE = true;
   ```
4. Busca la línea:
   ```javascript
   const FIREBASE_STORAGE_BUCKET = "tu-proyecto.appspot.com";
   ```
5. Reemplázala con tu bucket (del paso 4):
   ```javascript
   const FIREBASE_STORAGE_BUCKET = "tu-proyecto.appspot.com"; // Tu bucket real
   ```

### 8. Probar Localmente (2 minutos)

1. Abre `web/index.html` en tu navegador
2. Verifica que las imágenes se cargan correctamente
3. Abre la consola del navegador (F12) y verifica que no hay errores 404

### 9. Hacer Push a GitHub (Ahora será rápido)

```powershell
# Agregar solo los archivos de código (sin imágenes)
git add web/index.html backend/upload_images_firebase.py backend/firebase-credentials.json .gitignore
git commit -m "Configurar Firebase Storage para imágenes"
git push origin main
```

**Nota**: Asegúrate de que `web/images/` esté en `.gitignore` para no subir las imágenes a GitHub.

### 10. Desplegar en Netlify

1. Netlify detectará automáticamente los cambios
2. El deploy será mucho más rápido (solo HTML/JS, no imágenes)
3. Las imágenes se cargarán desde Firebase Storage

## 🔒 Seguridad

- Las imágenes son **públicas** (cualquiera con la URL puede verlas)
- Si necesitas privacidad, puedes configurar autenticación en Firebase
- Para uso médico, considera configurar reglas más estrictas

## 💰 Costos

**Firebase Storage Free Tier:**
- 5 GB de almacenamiento gratis
- 1 GB/día de descarga gratis
- Con 962 imágenes (~2.8 GB), estarás dentro del tier gratuito

**Si superas los límites:**
- Almacenamiento: ~$0.026/GB/mes
- Descarga: ~$0.12/GB

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo de credenciales"
- Verifica que el archivo JSON esté en `backend/firebase-credentials.json`
- Verifica que la ruta sea correcta

### Error: "Permission denied" al subir
- Verifica que las reglas de Storage permitan escritura (temporalmente)
- O usa la consola de Firebase para subir manualmente

### Las imágenes no se cargan en el navegador
- Verifica que `USE_FIREBASE_STORAGE = true`
- Verifica que el bucket sea correcto
- Abre la consola del navegador (F12) para ver errores
- Verifica que las imágenes estén en Firebase Storage → Files

### Las imágenes se cargan muy lento
- Firebase Storage es rápido, pero depende de tu conexión
- Considera usar Cloud CDN (Cloudflare) delante de Firebase

## ✅ Checklist Final

- [ ] Proyecto creado en Firebase
- [ ] Storage habilitado
- [ ] Reglas configuradas (lectura pública)
- [ ] Credenciales descargadas
- [ ] Imágenes subidas a Firebase Storage
- [ ] `USE_FIREBASE_STORAGE = true` en `web/index.html`
- [ ] Bucket configurado correctamente
- [ ] Probado localmente
- [ ] Push a GitHub (sin imágenes)
- [ ] Deploy en Netlify exitoso

## 🎉 ¡Listo!

Ahora tu herramienta funciona con Firebase Storage:
- GitHub: Solo código (liviano)
- Netlify: Deploy rápido
- Firebase: Almacena y sirve las imágenes
- Todo funciona igual que antes, solo cambia dónde están las imágenes
