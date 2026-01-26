# Instrucciones: Usar modelos entrenados con Folds

## Paso 1: Activar el entorno virtual

Desde PowerShell, en el directorio del proyecto:

```powershell
# Navegar al directorio del proyecto (si no estás ahí)
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"

# Activar el entorno virtual
..\.venv\Scripts\activate

# Deberías ver algo como:
# (.venv) PS D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool>
```

## Paso 2: Verificar cuántas imágenes de test hay

Antes de generar las predicciones, verifica cuántas imágenes tienes:

```powershell
python backend/count_test_images.py ^
  --lesion callos ^
  --scenario all_weeks ^
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority"
```

Esto te mostrará:
- Total de imágenes en cada carpeta
- Distribución por fold
- Imágenes encontradas vs faltantes

## Paso 3: Generar predicciones para la web

### Opción A: Ensemble (todos los folds) - RECOMENDADO

Usa todos los folds entrenados para mejor rendimiento:

```powershell
python backend/export_predictions_folds.py ^
  --lesion callos ^
  --scenario all_weeks ^
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority" ^
  --out-root "D:\PLesion_upch\Fase3_piloto_entrenamientos\Entrenamientos_2026\output" ^
  --web-dir "web" ^
  --arch UnetPlusPlus ^
  --encoder timm-efficientnet-b5 ^
  --fold -1 ^
  --threshold 0.50
```

### Opción B: Fold específico

Si quieres probar con un solo fold:

```powershell
python backend/export_predictions_folds.py ^
  --lesion callos ^
  --scenario all_weeks ^
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority" ^
  --out-root "D:\PLesion_upch\Fase3_piloto_entrenamientos\Entrenamientos_2026\output" ^
  --web-dir "web" ^
  --arch UnetPlusPlus ^
  --encoder timm-efficientnet-b5 ^
  --fold 0 ^
  --threshold 0.50
```

### Opción C: Comparar diferentes configuraciones

Si quieres comparar diferentes umbrales o modelos sin sobrescribir:

```powershell
# Configuración 1
python backend/export_predictions_folds.py ^
  --lesion callos ^
  --scenario all_weeks ^
  --consensus-root "..." ^
  --out-root "..." ^
  --web-dir "web" ^
  --arch UnetPlusPlus ^
  --encoder timm-efficientnet-b5 ^
  --fold -1 ^
  --threshold 0.50 ^
  --data-js-name "data_threshold_050.js"

# Configuración 2
python backend/export_predictions_folds.py ^
  --lesion callos ^
  --scenario all_weeks ^
  --consensus-root "..." ^
  --out-root "..." ^
  --web-dir "web" ^
  --arch UnetPlusPlus ^
  --encoder timm-efficientnet-b5 ^
  --fold -1 ^
  --threshold 0.40 ^
  --data-js-name "data_threshold_040.js"
```

Luego cambia en `web/index.html`:
```html
<script src="data_threshold_050.js"></script>  <!-- o data_threshold_040.js -->
```

## Parámetros disponibles

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--lesion` | Tipo de lesión | `callos` |
| `--scenario` | Escenario de splits | `all_weeks` |
| `--consensus-root` | Raíz del dataset | `D:\...\consensus_dataset_majority` |
| `--out-root` | Raíz de outputs de entrenamiento | `D:\...\Entrenamientos_2026\output` |
| `--web-dir` | Directorio de salida para web | `web` |
| `--arch` | Arquitectura | `UnetPlusPlus` |
| `--encoder` | Encoder | `timm-efficientnet-b5` |
| `--encoder-weights` | Pesos del encoder | `noisy-student` |
| `--fold` | Fold a usar (-1 = ensemble) | `-1` o `0`, `1`, `2`, etc. |
| `--threshold` | Umbral de binarización | `0.50` |
| `--min-area` | Área mínima para filtrar | `0` (no filtrar) |
| `--data-js-name` | Nombre del archivo data.js | `data.js` |

## Estructura esperada

El script espera esta estructura:

```
consensus_dataset_majority/
  callos/
    images/              # Imágenes originales
    images_clean/        # Imágenes limpias (prioridad)
    masks/               # Máscaras ground truth
    splits/
      kfold_all_weeks.csv

Entrenamientos_2026/
  output/
    callos/
      all_weeks/
        UnetPlusPlus__timm-efficientnet-b5/
          fold_0/
            checkpoints/
              best_model.pth
            optimal_threshold.json
          fold_1/
            ...
```

## Diferencias con tu predict.py

Este script (`export_predictions_folds.py`) está adaptado de tu `predict.py` pero:

✅ **Mantiene:**
- Sliding window con TTA
- Carga de múltiples folds (ensemble)
- Misma lógica de inferencia
- Uso de optimal_threshold.json

✅ **Adaptado para:**
- Generar formato para la herramienta web
- Extraer polígonos de lesiones
- Guardar imágenes procesadas
- Generar data.js

❌ **No incluye:**
- Cálculo de métricas (no hay ground truth en la web)
- Visualizaciones de comparación
- Reportes CSV de métricas

## Troubleshooting

### Error: "No se encontraron módulos locales"
- Asegúrate de estar en el directorio correcto
- O ajusta PYTHONPATH para incluir el directorio de entrenamiento

### Error: "Checkpoint no encontrado"
- Verifica que la ruta `--out-root` sea correcta
- Verifica que los folds estén en `fold_0/checkpoints/best_model.pth`

### Error: "No se encontró el CSV de splits"
- Verifica que `--consensus-root` y `--scenario` sean correctos
- El CSV debe estar en: `{consensus-root}/{lesion}/splits/kfold_{scenario}.csv`

### Las predicciones se ven mal
- Ajusta `--threshold` (prueba 0.40, 0.50, 0.60)
- Usa `--min-area` para filtrar ruido pequeño (ej: `--min-area 50`)

## Ejemplo completo de uso

```powershell
# 1. Activar entorno
..\.venv\Scripts\activate

# 2. Verificar imágenes
python backend/count_test_images.py ^
  --lesion callos ^
  --scenario all_weeks ^
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority"

# 3. Generar predicciones (ensemble)
python backend/export_predictions_folds.py ^
  --lesion callos ^
  --scenario all_weeks ^
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority" ^
  --out-root "D:\PLesion_upch\Fase3_piloto_entrenamientos\Entrenamientos_2026\output" ^
  --web-dir "web" ^
  --arch UnetPlusPlus ^
  --encoder timm-efficientnet-b5 ^
  --fold -1 ^
  --threshold 0.50

# 4. Abrir web/index.html en el navegador
```
