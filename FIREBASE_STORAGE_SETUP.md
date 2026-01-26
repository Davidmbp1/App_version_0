# Configuración de Firebase Storage para Imágenes

## Ventajas
✅ **No necesitas cambiar HTML/CSS/JS** - Solo cambias cómo se cargan las URLs
✅ **GitHub queda liviano** - Solo código, no imágenes
✅ **Netlify funciona perfecto** - Solo sirve HTML/JS pequeño
✅ **Escalable** - Firebase Storage maneja el tráfico de imágenes

## Pasos

### 1. Crear Proyecto en Firebase
1. Ve a: https://console.firebase.google.com/
2. Click en **"Add project"** o selecciona uno existente
3. Sigue los pasos (puedes desactivar Google Analytics si quieres)

### 2. Habilitar Firebase Storage
1. En el proyecto, ve a **Storage** (en el menú izquierdo)
2. Click en **"Get started"**
3. Selecciona **"Start in test mode"** (por ahora, luego puedes cambiar reglas)
4. Selecciona una ubicación (ej: `us-central1`)
5. Click **"Done"**

### 3. Obtener Configuración
1. Ve a **Project Settings** (⚙️) → **General**
2. Baja hasta **"Your apps"**
3. Click en el ícono **`</>`** (Web)
4. Registra el app (nombre: "Callos Annotation Tool")
5. **Copia** el objeto de configuración que aparece, algo como:
```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

### 4. Configurar Reglas de Storage (Importante para acceso público)
1. Ve a **Storage** → **Rules**
2. Reemplaza las reglas con:
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /images/{imageName} {
      allow read: if true;  // Permite lectura pública
      allow write: if false; // Solo tú puedes escribir (desde tu máquina)
    }
  }
}
```
3. Click **"Publish"**

### 5. Subir Imágenes a Firebase Storage
Usa el script `backend/upload_images_firebase.py` que crearemos.

### 6. Actualizar HTML
El archivo `web/index.html` se modificará para usar URLs de Firebase Storage en lugar de rutas locales.

## Costos
- **Firebase Storage Free Tier**: 5 GB de almacenamiento, 1 GB/día de descarga
- Con 962 imágenes (~2.8 GB), estarás dentro del tier gratuito
- Si superas los límites, los costos son muy bajos (~$0.026/GB almacenamiento, $0.12/GB descarga)

## Alternativa: Cloudinary (Más fácil, pero con límites)
Si prefieres algo más simple:
- Cloudinary tiene 25 GB gratis
- Subes imágenes por drag & drop
- Obtienes URLs directas
- No requiere configuración de reglas

¿Prefieres Firebase Storage o Cloudinary?
