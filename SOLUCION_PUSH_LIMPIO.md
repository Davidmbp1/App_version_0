# Solución: Push Limpio a GitHub

## Problema
El historial de Git contiene ~2.79 GB de imágenes, lo que causa el error HTTP 500 al hacer push.

## Solución: Repositorio Limpio

Vamos a crear un nuevo commit inicial limpio sin el historial pesado.

### Opción 1: Crear Nuevo Branch Limpio (RECOMENDADO)

```powershell
# 1. Crear un nuevo branch sin historial
git checkout --orphan clean-main

# 2. Agregar todos los archivos actuales (sin imágenes)
git add .

# 3. Hacer commit inicial
git commit -m "Initial commit: Callos Annotation Tool con Firebase Storage"

# 4. Eliminar el branch main antiguo
git branch -D main

# 5. Renombrar el branch limpio a main
git branch -m main

# 6. Forzar push (esto reemplazará el historial en GitHub)
git push -f origin main
```

### Opción 2: Si el Push Sigue Fallando

Si el push sigue fallando, podemos hacer push en partes más pequeñas o usar GitHub CLI.

## Verificación

Después del push:
1. Ve a: https://github.com/Davidmbp1/App_version_0
2. Verifica que el repositorio sea mucho más pequeño
3. Verifica que no haya carpeta `web/images/` en el repositorio
