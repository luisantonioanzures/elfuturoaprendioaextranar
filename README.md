# El futuro aprendió a extrañar — sitio de lectura

Sitio estático preparado para GitHub Pages. **No contiene el texto del libro** hasta que el autor suba su PDF.

## Cómo publicarlo gratis

1. En https://github.com/new crea un repositorio **público** llamado exactamente `el-futuro-aprendio-a-extranar` (sin acentos ni espacios). Marca **Add a README file** si GitHub lo ofrece.
2. En la pestaña **Code** del repositorio, selecciona **Add file → Upload files** y sube el archivo `index.html` de este paquete. También puedes subir este `README.md` si quieres, aunque no es obligatorio.
3. Exporta el manuscrito completo como PDF y renómbralo exactamente `libro.pdf` (minúsculas). Súbelo a la **raíz del mismo repositorio**, junto a `index.html`, usando **Add file → Upload files**. No subas todavía borradores que no quieras compartir públicamente.
4. Opcional: sube una imagen de tu portada con el nombre `portada.jpg` para reemplazar la cubierta ilustrativa de ejemplo. Lo ideal es una imagen vertical de buena calidad.
5. Ve a **Settings → Pages** y en **Build and deployment** selecciona **Source: Deploy from a branch**, **Branch: main**, carpeta **/(root)** y **Save**.
6. Abre `https://TUUSUARIO.github.io/el-futuro-aprendio-a-extranar/` cambiando TUUSUARIO por el nombre exacto de tu cuenta de GitHub. La activación puede tardar hasta 10 minutos después de guardar/publicar.

## Observaciones

- El título y el nombre del autor están escritos en `index.html`. Puedes modificarlos editando ese archivo.
- El lector usa PDF.js por CDN para dibujar las páginas: el lector necesita internet también para cargar ese código.
- Los botones permiten pasar páginas, ampliar/reducir, compartir y abrir el PDF original. En computadora funcionan también las teclas de flecha.
- GitHub Pages es público. **Todo PDF que publiques ahí será accesible y potencialmente descargable por otras personas**, aunque el sitio principal use un visor. No es un sistema anticopia o de venta protegida.
- Para que la URL tenga exactamente el título sin el nombre de GitHub, necesitarías adquirir un dominio propio y configurarlo en GitHub Pages.

Información oficial: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
