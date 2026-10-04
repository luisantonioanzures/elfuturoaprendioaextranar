# El futuro aprendió a extrañar — editor privado

Una web para leer tu EPUB y una entrada editorial minimalista en `/edit/`.

## Cómo activarlo (una sola vez)

1. Abre tu repositorio de GitHub donde ahora tienes el libro. Descomprime el ZIP y **sube todos los archivos y carpetas**, incluida `.pages.yml` y `.github/workflows/publicar-libro.yml`, al nivel principal del repositorio. **No subas la carpeta envolvente** `El_futuro_editor_GitHub`: sube lo que está dentro. En iPhone, puede ser más cómodo realizar la primera carga desde una computadora. La carpeta `.github` y el archivo `.pages.yml` son imprescindibles.
2. En GitHub, entra en **Settings → Pages → Build and deployment → Source** y selecciona **GitHub Actions**. Si ya publicabas desde `main`, cambiar esta opción es necesario para generar el EPUB automáticamente.
3. En la pestaña **Actions**, verifica que se ejecutó **Publicar libro digital** y terminó correctamente. Si no arranca, abre ese workflow y pulsa **Run workflow**.
4. Abre tu web con `/edit/` al final de la URL (por ejemplo `https://luisantonioanzures.github.io/edit/` si ese es tu sitio). Pulsa **Continuar con GitHub**. Entrarás en `app.pagescms.org`, un servicio externo que administra archivos de GitHub.
5. En Pages CMS, inicia sesión con GitHub y autoriza la **GitHub App de Pages CMS únicamente en el repositorio del libro**. Elige ese repositorio, rama `main`, y abre **El futuro aprendió a extrañar**. Si Pages CMS no te deja seleccionar el repositorio, revisa que la app tenga acceso a él.
6. Cambia la dedicatoria, la nota o el contenido de un capítulo y pulsa **Save / Guardar**. Pages CMS guardará los cambios en `contenido.json` del repositorio. GitHub Actions los convertirá a `libro.epub` y publicará el lector.
7. Espera a que termine el workflow en **Actions** y recarga el libro (si no ves los cambios, recarga sin caché o espera un momento).

## Qué protege el acceso

- La dirección `/edit/` **no está oculta**. Cualquier persona podría verla, pero **solo las cuentas con permiso de escritura en el repositorio** pueden guardar cambios después de autenticar con GitHub.
- **No hay contraseñas incrustadas** en el HTML. No pegues tu contraseña ni tokens personales en un archivo web o en `contenido.json`.
- La interfaz de bienvenida beige está en tu sitio; la pantalla de autenticación y el editor se abren en Pages CMS. No es un login propio ni guarda usuarios de GitHub en tu web.

## Archivos importantes

- `index.html`: lector público que ya utilizabas, preservado.
- `edit/index.html`: acceso de autor beige.
- `contenido.json`: contenido editable con el CMS. Puedes añadir capítulos en la lista `capitulos`.
- `.pages.yml`: indica los campos disponibles en Pages CMS.
- `portada.jpg`: portada original del EPUB.
- `scripts/construir_epub.py`: construye un EPUB 3 de texto adaptable desde `contenido.json`.
- `.github/workflows/publicar-libro.yml`: regenera el EPUB y despliega ambos sitios al guardar.
- `libro.epub`: EPUB inicial; en la publicación se regenera desde `contenido.json`.

## Nota sobre el progreso del lector

El EPUB generado preserva dedicatoria, nota, capítulo(s) y portada. Si agregas muchos capítulos o cambias mucho la extensión, el visor intenta mantener la **posición proporcional** de avance cuando el número de páginas cambia, pero ese porcentaje no garantiza que vuelva exactamente a la misma frase.

## Si no se abre /edit

El repositorio puede ser `luisantonioanzures.github.io` (sitio principal) o un proyecto bajo otra ruta. En el segundo caso la URL es `https://USUARIO.github.io/NOMBRE-DEL-REPOSITORIO/edit/`. Revisa también que GitHub Pages esté desplegando desde **GitHub Actions** y que el workflow haya concluido.

## Uso del EPUB fuera de tu web

El workflow genera la edición actualizada para servirla en el sitio, no hace un commit del EPUB a la rama `main`. Para obtener una copia EPUB descargable de cada publicación, puedes abrir la URL pública `/libro.epub` después del despliegue.
