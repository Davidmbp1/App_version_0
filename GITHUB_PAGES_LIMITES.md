# Límites de GitHub Pages

## Límites de Almacenamiento y Ancho de Banda

### Repositorios Públicos (Gratis)
- **Almacenamiento:** 1 GB máximo por repositorio
- **Ancho de banda:** 100 GB/mes
- **Tamaño de archivo individual:** 100 MB máximo

### Repositorios Privados
- **GitHub Pages privado:** Requiere **GitHub Pro** ($4/mes por usuario)
- Con GitHub Pro, los límites son los mismos que repositorios públicos

## ¿Puede GitHub Pages manejar todas tus imágenes?

### Verificación Rápida

Ejecuta este comando para ver el tamaño total:

```powershell
# Ver tamaño de imágenes
Get-ChildItem -Path "web\images" -File -Recurse | 
    Measure-Object -Property Length -Sum | 
    Select-Object @{Name='TotalMB';Expression={[math]::Round($_.Sum / 1MB, 2)}}

# Ver tamaño de data.js
(Get-Item "web\data.js").Length / 1MB
```

### Escenarios

#### ✅ **Menos de 500 MB** → GitHub Pages es perfecto
- Sin problemas
- Rápido y confiable

#### ⚠️ **500 MB - 1 GB** → GitHub Pages funciona, pero considera alternativas
- Funciona, pero cerca del límite
- Si agregas más imágenes en el futuro, podrías exceder el límite
- Considera Netlify o Vercel (límites más generosos)

#### ❌ **Más de 1 GB** → Necesitas otra solución
- GitHub Pages no aceptará el repositorio
- Opciones:
  1. **Netlify** - 100 GB/mes gratis, sin límite de almacenamiento por sitio
  2. **Vercel** - Similar a Netlify
  3. **Servidor propio** - Control total

## Alternativas si GitHub Pages no es suficiente

### 1. Netlify (Recomendado para proyectos grandes)
- ✅ **100 GB/mes** de ancho de banda gratis
- ✅ **Sin límite** de almacenamiento por sitio
- ✅ Muy fácil de usar
- ✅ HTTPS automático

### 2. Vercel
- ✅ Similar a Netlify
- ✅ 100 GB/mes gratis
- ✅ Buen rendimiento

### 3. Servidor Local/Interno
- ✅ Sin límites
- ✅ Control total
- ⚠️ Requiere mantener el servidor activo

## Optimización de Imágenes (Opcional)

Si tus imágenes son muy grandes, puedes optimizarlas antes de subir:

```powershell
# Instalar herramienta de optimización (opcional)
# pip install pillow

# Script de ejemplo para optimizar imágenes
python -c "
from PIL import Image
import os
from pathlib import Path

images_dir = Path('web/images')
for img_path in images_dir.glob('*.png'):
    img = Image.open(img_path)
    # Reducir calidad si es necesario
    img.save(img_path, 'PNG', optimize=True)
    print(f'Optimizado: {img_path.name}')
"
```

## Recomendación Final

1. **Verifica el tamaño** con el script `desplegar_github_pages.ps1`
2. **Si es < 500 MB:** Usa GitHub Pages
3. **Si es 500 MB - 1 GB:** Considera Netlify para más espacio
4. **Si es > 1 GB:** Usa Netlify o servidor propio
