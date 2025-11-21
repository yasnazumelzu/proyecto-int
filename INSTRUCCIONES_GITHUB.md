# Instrucciones para subir el proyecto a GitHub

## Paso 1: Crear el repositorio en GitHub

1. Ve a https://github.com y inicia sesión
2. Haz clic en el botón "+" (arriba a la derecha) → "New repository"
3. Nombre del repositorio: `sistema-hospital-herminda-martin` (o el que prefieras)
4. Descripción: "Sistema de gestión hospitalaria - Hospital Clínico Herminda Martín"
5. Elige si será Público o Privado
6. **NO marques** "Initialize this repository with a README"
7. Haz clic en "Create repository"

## Paso 2: Conectar tu repositorio local con GitHub

Después de crear el repositorio, GitHub te mostrará una página con instrucciones. 
Ejecuta estos comandos (reemplaza TU_USUARIO y NOMBRE_REPOSITORIO):

```bash
# Agregar el repositorio remoto de GitHub
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPOSITORIO.git

# Cambiar el nombre de la rama a main (si es necesario)
git branch -M main

# Subir tu código a GitHub
git push -u origin main
```

## Ejemplo completo:

Si tu usuario de GitHub es `yaspa` y el repositorio se llama `sistema-hospital-herminda-martin`:

```bash
git remote add origin https://github.com/yaspa/sistema-hospital-herminda-martin.git
git branch -M main
git push -u origin main
```

## Si te pide autenticación:

GitHub ya no acepta contraseñas. Necesitas usar un **Personal Access Token**:

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Haz clic en "Generate new token (classic)"
3. Dale un nombre y selecciona los permisos: `repo` (todos los permisos de repositorio)
4. Copia el token generado
5. Cuando git te pida la contraseña, usa el token en lugar de tu contraseña

## Comandos útiles después:

```bash
# Ver el estado de tus cambios
git status

# Agregar cambios
git add .

# Guardar cambios
git commit -m "Descripción de los cambios"

# Subir cambios a GitHub
git push
```

