# Pasos para Configurar Netlify - Publish Directory

## Paso 1: Hacer clic en "Configure"
En la sección "Build settings", busca el botón **"Configure"** (debe estar cerca de "Runtime" o "Build settings").

## Paso 2: Cambiar "Publish directory"
1. Se abrirá un formulario o modal
2. Busca el campo **"Publish directory"**
3. Cambia el valor de `Not set` o `/` a: **`web`**
4. **NO cambies** "Base directory" (déjalo en `/`)
5. **NO cambies** "Build command" (déjalo vacío)

## Paso 3: Guardar
- Haz clic en **"Save"** o **"Update"**

## Paso 4: Hacer un nuevo Deploy
1. Ve a la pestaña **"Deploys"** (en el menú izquierdo)
2. Haz clic en **"Trigger deploy"** → **"Deploy site"**
3. Espera a que termine el deploy

## Paso 5: Verificar
Después del deploy, en **"Deploy file browser"** deberías ver:
```
web/
├── index.html
├── data.js
└── images/
    └── ... (962 imágenes)
```

## Si no encuentras "Configure"
Si no ves el botón "Configure", busca un botón de edición (lápiz ✏️) o haz clic directamente en el campo "Publish directory" si es editable.
