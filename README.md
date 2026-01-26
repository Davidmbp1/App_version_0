# Callos Annotation Tool

Herramienta web para que médicos revisen y etiqueten predicciones de un modelo de segmentación (U-Net++) de callos.

## Estructura

- `backend/`: scripts de Python para ejecutar inferencia y generar datos para la interfaz web.
- `web/`: aplicación web estática que mostrará imágenes y permitirá marcar si una lesión es callo o no.
- `models/`: carpeta local (no versionada) donde colocar el checkpoint .pth del modelo.

## Inicio Rápido

### 1. Generar Predicciones

```powershell
# Activar entorno virtual
.\.venv\Scripts\activate

# Generar predicciones (ajusta los parámetros según tu caso)
python backend/export_predictions_folds.py --lesion callos --scenario all_weeks --consensus-root "ruta" --out-root "ruta" --web-dir "web" --arch UnetPlusPlus --encoder timm-efficientnet-b5 --fold -1 --threshold 0.7
```

### 2. Desplegar para Uso

**Opción A: Servidor Local (Recomendado para uso interno)**

```powershell
# Iniciar servidor web
python servidor_local.py

# O usar el script PowerShell
.\servidor_local.ps1
```

Luego abre en el navegador: `http://localhost:8000`

Para acceso desde otras computadoras en la misma red, el script mostrará la IP local (ej: `http://192.168.1.100:8000`).

**Opción B: Despliegue en Netlify (Recomendado para proyectos grandes)**

⚠️ **IMPORTANTE:** Tu proyecto es **2.8 GB**, por lo que **GitHub Pages NO funcionará** (límite 1 GB).

**Despliegue rápido en Netlify:**

```powershell
# Usa el script automatizado
.\desplegar_netlify.ps1
```

El script te guiará paso a paso. Ver `desplegar_netlify_permanente.md` para instrucciones detalladas.

**Otras opciones:**
- **Servidor Local** - Para uso interno (ver `DESPLIEGUE.md` Opción 1)
- **Vercel** - Alternativa similar a Netlify

Ver `RESUMEN_DESPLIEGUE.md` para un análisis completo de opciones.

## Características

- ✅ Interfaz intuitiva para médicos
- ✅ Leyenda de colores y barra de progreso
- ✅ Soporte para "Otra lesión" con especificación de tipo
- ✅ Exportación a CSV/JSON
- ✅ Guardado automático en el navegador

## Documentación

- `DESPLIEGUE.md`: Guía completa de despliegue
- `backend/INSTRUCCIONES_FOLDS.md`: Instrucciones para usar modelos con k-folds
- `backend/README_USO_MODELOS.md`: Guía de uso de diferentes arquitecturas
