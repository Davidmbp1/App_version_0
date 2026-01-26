# Resumen: Opciones de Despliegue para tu Proyecto

## ⚠️ Situación Actual

**Tamaño de tu proyecto:**
- Imágenes: **2.67 GB** (962 archivos)
- data.js: **134 MB**
- **Total: 2.8 GB**

## ❌ GitHub Pages NO es viable

**Límites de GitHub Pages:**
- Repositorio: **1 GB máximo** ❌ (tu proyecto es 2.8 GB)
- Archivo individual: **100 MB máximo** ❌ (data.js es 134 MB)

**Conclusión:** GitHub Pages rechazará tu repositorio por exceder los límites.

---

## ✅ Opciones Recomendadas

### 1. Netlify (RECOMENDADO) ⭐⭐⭐

**Ventajas:**
- ✅ **100 GB/mes** de ancho de banda gratis
- ✅ **Sin límite** de almacenamiento por sitio
- ✅ Acepta archivos de hasta 100 MB (pero puedes dividir data.js si es necesario)
- ✅ Muy fácil de usar
- ✅ HTTPS automático
- ✅ Permanente y gratuito

**Pasos:**
1. Crea cuenta en https://www.netlify.com
2. Crea repositorio en GitHub con tu código
3. Conecta Netlify con GitHub
4. Configura: Build command (vacío), Publish directory: `web`
5. ¡Listo!

**Ver:** `desplegar_netlify_permanente.md` para instrucciones detalladas.

---

### 2. Vercel (Alternativa a Netlify)

**Ventajas:**
- ✅ Similar a Netlify
- ✅ 100 GB/mes gratis
- ✅ Buen rendimiento

**Pasos:**
```powershell
npm install -g vercel
cd web
vercel
```

---

### 3. Servidor Local/Interno (Para uso en hospital)

**Ventajas:**
- ✅ Sin límites de tamaño
- ✅ Control total
- ✅ Datos privados en tu red

**Pasos:**
```powershell
python servidor_local.py
```

Los médicos acceden desde: `http://TU_IP:8000`

**Ver:** `DESPLIEGUE.md` Opción 1 para más detalles.

---

## Solución para data.js (134 MB)

Si Netlify/Vercel tienen problemas con archivos >100 MB, puedes:

### Opción A: Dividir data.js en múltiples archivos

```python
# Script para dividir data.js
import json

# Cargar data.js
with open('web/data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    # Extraer el array de casos
    data_str = content.replace('const cases = ', '').replace(';', '')
    cases = json.loads(data_str)

# Dividir en chunks de 500 casos
chunk_size = 500
for i in range(0, len(cases), chunk_size):
    chunk = cases[i:i+chunk_size]
    with open(f'web/data_{i//chunk_size}.js', 'w', encoding='utf-8') as f:
        f.write(f'const cases_{i//chunk_size} = {json.dumps(chunk, ensure_ascii=False)};')
```

Luego modificar `index.html` para cargar múltiples archivos.

### Opción B: Comprimir data.js

```python
import gzip
import shutil

with open('web/data.js', 'rb') as f_in:
    with gzip.open('web/data.js.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
```

Y modificar `index.html` para descomprimir en el navegador.

---

## Recomendación Final

**Para tu caso (2.8 GB):**

1. **Primera opción:** Netlify con repositorio Git
   - Acepta el tamaño total
   - Permanente y gratuito
   - Fácil de configurar

2. **Segunda opción:** Servidor local
   - Si solo es para uso interno en el hospital
   - Sin límites
   - Control total

3. **Si Netlify rechaza data.js (134 MB):**
   - Divide data.js en múltiples archivos más pequeños
   - O comprime y descomprime en el navegador

---

## Próximos Pasos

1. **Verifica el tamaño:** `python verificar_tamano.py`
2. **Elige la opción:**
   - Netlify → Ver `desplegar_netlify_permanente.md`
   - Servidor local → Ver `DESPLIEGUE.md` Opción 1
3. **Si necesitas dividir data.js:** Puedo crear un script para hacerlo
