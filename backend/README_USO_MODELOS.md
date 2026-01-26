# Guía: Cómo usar diferentes modelos con el mismo script

## Respuesta rápida

**SÍ, puedes hacerlo en este mismo proyecto.** No necesitas cambiar de entorno. Solo necesitas:

1. Tener el checkpoint (`.pth`) del otro modelo
2. Saber qué arquitectura y encoder usó ese modelo
3. Ejecutar el script con los parámetros correctos

## ¿Dónde hacerlo?

### Opción 1: En este proyecto (RECOMENDADO)
- ✅ Ya tienes todas las dependencias instaladas
- ✅ El script está listo para usar
- ✅ Solo cambias los parámetros de línea de comandos

### Opción 2: En tu entorno de entrenamiento
- Solo si necesitas instalar dependencias adicionales
- O si el modelo requiere código personalizado

**Recomendación:** Usa este proyecto. Es más simple y ya está configurado.

## Cómo usar el script con otro modelo

### Paso 1: Identifica tu modelo

Necesitas saber:
- **Arquitectura**: ¿Es UNet++, UNet, DeepLabV3+, FPN, etc.?
- **Encoder**: ¿Qué backbone usó? (EfficientNet-B5, ResNet34, etc.)
- **Tamaño de entrada**: ¿Qué tamaño de imagen usó? (ej: 832x832, 512x512, etc.)

### Paso 2: Ejecuta el script

#### Ejemplo 1: Modelo UNet++ con EfficientNet-B5 (como el actual)
```bash
python backend/export_predictions.py ^
  --images "ruta/a/tus/imagenes" ^
  --model-ckpt "ruta/al/checkpoint.pth" ^
  --out-dir "web" ^
  --architecture "UnetPlusPlus" ^
  --encoder "timm-efficientnet-b5" ^
  --img-long 832 ^
  --crop 832
```

#### Ejemplo 2: Modelo UNet con ResNet34
```bash
python backend/export_predictions.py ^
  --images "ruta/a/tus/imagenes" ^
  --model-ckpt "ruta/al/otro_modelo.pth" ^
  --out-dir "web" ^
  --architecture "Unet" ^
  --encoder "resnet34" ^
  --img-long 512 ^
  --crop 512
```

#### Ejemplo 3: Modelo DeepLabV3+ con EfficientNet-B4
```bash
python backend/export_predictions.py ^
  --images "ruta/a/tus/imagenes" ^
  --model-ckpt "ruta/al/modelo_deeplab.pth" ^
  --out-dir "web" ^
  --architecture "DeepLabV3Plus" ^
  --encoder "timm-efficientnet-b4" ^
  --img-long 832 ^
  --crop 832
```

### Paso 3: Comparar modelos (opcional)

Si quieres comparar dos modelos sin sobrescribir, usa `--data-js-name`:

```bash
# Generar con modelo 1
python backend/export_predictions.py ^
  --images "ruta/imagenes" ^
  --model-ckpt "modelo1.pth" ^
  --out-dir "web" ^
  --data-js-name "data_modelo1.js"

# Generar con modelo 2
python backend/export_predictions.py ^
  --images "ruta/imagenes" ^
  --model-ckpt "modelo2.pth" ^
  --out-dir "web" ^
  --data-js-name "data_modelo2.js"
```

Luego en `index.html`, cambia temporalmente:
```html
<script src="data_modelo1.js"></script>  <!-- o data_modelo2.js -->
```

## Parámetros disponibles

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `--images` | Carpeta con imágenes originales | **Requerido** |
| `--model-ckpt` | Ruta al checkpoint .pth | **Requerido** |
| `--out-dir` | Carpeta de salida (ej: web) | **Requerido** |
| `--architecture` | Arquitectura: UnetPlusPlus, Unet, DeepLabV3Plus, FPN, PSPNet, etc. | `UnetPlusPlus` |
| `--encoder` | Encoder: timm-efficientnet-b5, resnet34, efficientnet-b4, etc. | `timm-efficientnet-b5` |
| `--img-long` | Tamaño del lado largo para redimensionar | `832` |
| `--crop` | Tamaño del crop cuadrado | `832` |
| `--thr` | Umbral de probabilidad (0.0-1.0) | `0.30` |
| `--min-area` | Área mínima de píxeles para filtrar | `0` (no filtrar) |
| `--batch-size` | Tamaño del batch | `2` |
| `--data-js-name` | Nombre del archivo data.js de salida | `data.js` |

## Arquitecturas soportadas

El script soporta todas las arquitecturas de `segmentation-models-pytorch`:

- `UnetPlusPlus`
- `Unet`
- `DeepLabV3Plus`
- `FPN`
- `PSPNet`
- `Linknet`
- `PAN`
- Y más...

## Encoders comunes

- `timm-efficientnet-b5`, `timm-efficientnet-b4`, `timm-efficientnet-b3`
- `resnet34`, `resnet50`, `resnet101`
- `efficientnet-b0` hasta `efficientnet-b7`
- `densenet121`, `densenet169`
- Y muchos más...

## Troubleshooting

### Error: "Arquitectura 'X' no encontrada"
- Verifica que el nombre de la arquitectura sea exacto (case-sensitive)
- Debe coincidir con el nombre en `segmentation_models_pytorch`

### Error al cargar el checkpoint
- El script intenta cargar de diferentes formas:
  - `state["model_state_dict"]`
  - `state["state_dict"]`
  - `state` directamente
- Si falla, puede que el checkpoint tenga una estructura diferente

### Las predicciones se ven mal
- Verifica que `--img-long` y `--crop` coincidan con el entrenamiento
- Ajusta `--thr` (umbral) si hay muchos falsos positivos/negativos
- Usa `--min-area` para filtrar ruido pequeño

## Ejemplo completo

```bash
# Modelo original (UNet++ EfficientNet-B5)
python backend/export_predictions.py ^
  --images "D:/imagenes/test" ^
  --model-ckpt "D:/modelos/unetpp_effb5.pth" ^
  --out-dir "web" ^
  --architecture "UnetPlusPlus" ^
  --encoder "timm-efficientnet-b5" ^
  --img-long 832 ^
  --crop 832 ^
  --thr 0.30

# Nuevo modelo (UNet ResNet34)
python backend/export_predictions.py ^
  --images "D:/imagenes/test" ^
  --model-ckpt "D:/modelos/unet_resnet34.pth" ^
  --out-dir "web" ^
  --architecture "Unet" ^
  --encoder "resnet34" ^
  --img-long 512 ^
  --crop 512 ^
  --thr 0.35 ^
  --data-js-name "data_unet_resnet34.js"
```

## Notas importantes

1. **Mismas imágenes**: Puedes usar exactamente las mismas imágenes con diferentes modelos
2. **Mismo entorno**: No necesitas cambiar de entorno, solo cambiar parámetros
3. **Comparación**: Usa `--data-js-name` para generar múltiples archivos y comparar
4. **Backup**: Si vas a sobrescribir `data.js`, haz backup primero
