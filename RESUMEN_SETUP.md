# Resumen: Configuración para usar tus modelos entrenados

## ✅ Lo que he creado

1. **`backend/export_predictions_folds.py`** - Script principal adaptado a tu sistema
   - Usa la misma lógica de sliding window que tu `predict.py`
   - Soporta ensemble (todos los folds) o fold individual
   - Genera `data.js` y imágenes para la web

2. **`backend/count_test_images.py`** - Script para contar imágenes
   - Muestra cuántas imágenes hay en cada carpeta
   - Distribución por fold
   - Verifica qué imágenes existen

3. **Scripts PowerShell** para facilitar el uso:
   - `activar_y_contar.ps1` - Activa entorno y cuenta imágenes
   - `generar_predicciones.ps1` - Genera predicciones fácilmente

4. **Documentación**:
   - `backend/INSTRUCCIONES_FOLDS.md` - Guía completa

## 🚀 Uso rápido

### Paso 1: Activar entorno y contar imágenes

```powershell
# Desde: D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool>

# Opción A: Usar script PowerShell
.\activar_y_contar.ps1

# Opción B: Manual
..\.venv\Scripts\activate
python backend/count_test_images.py --lesion callos --scenario all_weeks --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority"
```

### Paso 2: Generar predicciones

```powershell
# Opción A: Usar script PowerShell (ensemble, threshold 0.50)
.\generar_predicciones.ps1

# Opción B: Con parámetros personalizados
.\generar_predicciones.ps1 -Fold -1 -Threshold 0.50 -DataJsName "data.js"

# Opción C: Manual (más control)
python backend/export_predictions_folds.py `
  --lesion callos `
  --scenario all_weeks `
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority" `
  --out-root "D:\PLesion_upch\Fase3_piloto_entrenamientos\Entrenamientos_2026\output" `
  --web-dir "web" `
  --arch UnetPlusPlus `
  --encoder timm-efficientnet-b5 `
  --fold -1 `
  --threshold 0.50
```

### Paso 3: Abrir la herramienta web

Simplemente abre `web/index.html` en tu navegador.

## 📊 Respuestas a tus preguntas

### ¿Dónde hacerlo?
✅ **En este mismo proyecto** (`callos-annotation-tool`). No necesitas cambiar de entorno.

### ¿Cómo usar tus modelos entrenados?
✅ **Usa `export_predictions_folds.py`** que está adaptado a tu sistema:
- Lee los checkpoints de tus folds
- Usa la misma lógica de sliding window
- Soporta ensemble (todos los folds) o fold individual

### ¿Cuántas imágenes de test hay?
✅ **Ejecuta `count_test_images.py`** para ver:
- Total de imágenes
- Distribución por fold
- Imágenes encontradas vs faltantes

## 🔄 Comparación con tu predict.py

| Característica | Tu predict.py | export_predictions_folds.py |
|----------------|---------------|----------------------------|
| Sliding Window | ✅ | ✅ |
| TTA (Test Time Augmentation) | ✅ | ✅ |
| Ensemble (múltiples folds) | ✅ | ✅ |
| Carga optimal_threshold.json | ✅ | ✅ |
| **Genera data.js para web** | ❌ | ✅ |
| **Extrae polígonos** | ❌ | ✅ |
| **Guarda imágenes procesadas** | ❌ | ✅ |
| Calcula métricas | ✅ | ❌ (no hay GT en web) |
| Visualizaciones | ✅ | ❌ |

## 📝 Ejemplo completo

```powershell
# 1. Navegar al proyecto
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"

# 2. Activar entorno
..\.venv\Scripts\activate

# 3. Ver cuántas imágenes hay
python backend/count_test_images.py `
  --lesion callos `
  --scenario all_weeks `
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority"

# 4. Generar predicciones (ensemble)
python backend/export_predictions_folds.py `
  --lesion callos `
  --scenario all_weeks `
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority" `
  --out-root "D:\PLesion_upch\Fase3_piloto_entrenamientos\Entrenamientos_2026\output" `
  --web-dir "web" `
  --arch UnetPlusPlus `
  --encoder timm-efficientnet-b5 `
  --fold -1 `
  --threshold 0.50

# 5. Abrir web/index.html
```

## ⚙️ Parámetros importantes

- `--fold -1`: Usa todos los folds (ensemble) - **RECOMENDADO**
- `--fold 0`: Usa solo el fold 0
- `--threshold 0.50`: Umbral de binarización (ajusta según necesites)
- `--min-area 0`: Filtra componentes pequeñas (0 = no filtrar)

## 🐛 Troubleshooting

### Error: "No se encontraron módulos locales"
**Solución**: Asegúrate de que el directorio de entrenamiento esté en PYTHONPATH o ejecuta desde el directorio correcto.

### Error: "Checkpoint no encontrado"
**Solución**: Verifica que la ruta `--out-root` sea correcta y que los folds existan.

### Las predicciones se ven mal
**Solución**: 
- Ajusta `--threshold` (prueba 0.40, 0.50, 0.60)
- Usa `--min-area 50` para filtrar ruido pequeño

## 📚 Más información

- Ver `backend/INSTRUCCIONES_FOLDS.md` para guía detallada
- Ver `backend/README_USO_MODELOS.md` para usar otros modelos
