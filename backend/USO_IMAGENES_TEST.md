# Uso de Imágenes de TEST del CSV

## ✅ Cambios Realizados

El script `export_predictions_folds.py` ahora:

1. **Busca el CSV correcto**: 
   - Primero intenta `splits_all_weeks.csv`
   - Si no existe, usa `kfold_all_weeks.csv` como fallback

2. **Filtra solo imágenes de TEST**:
   - Lee la columna `split` del CSV
   - Filtra solo las filas donde `split == "test"`
   - Usa esas imágenes para generar las predicciones

3. **Usa los nombres de archivo del CSV**:
   - Si el CSV tiene `image_filename`, usa ese nombre exacto
   - Si no, busca por `stem` en las carpetas

## 📊 Estadísticas del CSV

Para `callos/splits/splits_all_weeks.csv`:
- **Train**: 4,485 imágenes
- **Val**: 961 imágenes  
- **Test**: 962 imágenes ← **Estas se usarán para la web**

## 🚀 Uso

El comando es el mismo, pero ahora automáticamente usará solo las imágenes de test:

```powershell
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

## 🔍 Verificación

El script mostrará:
```
[INFO] Total de registros en CSV: 6408
[INFO] Imágenes marcadas como TEST: 962
[OK] Filtrando solo imágenes de TEST
[INFO] Procesando 962 imágenes...
```

## 📝 Notas

- Si el CSV no tiene columna `split`, el script usará todas las imágenes (comportamiento anterior)
- Si no hay imágenes marcadas como "test", mostrará un warning y usará todas las imágenes
- Las máscaras se buscan automáticamente usando el `mask_filename` del CSV si está disponible
