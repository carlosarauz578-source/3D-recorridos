# Recorridos 3D

Proyecto de recorrido virtual creado con **3DVista Player v1901**.

## Contenido publicado

- `index.html`: archivo HTML original del recorrido **Dual Viewers**.
- Idioma configurado: español.

## Recursos que faltan para que el recorrido funcione

El HTML referencia archivos y carpetas externos que todavía no están incluidos en este repositorio. Para reproducir el tour desde GitHub Pages o localmente, deben agregarse conservando exactamente sus rutas relativas:

- `lib/tdvplayer.js`
- `lib/WebVRPolyfill.js`
- `lib/Hls.js`
- `lib/cursors/`
- `script.js`
- `script_general.js`
- `locale/es.txt`
- `media/` (mosaicos de panoramas y demás recursos)
- `socialThumbnail.jpg` y otros recursos referenciados, si se desean conservar.

## Fuente original

https://storage.net-fs.com/hosting/2727323/443/index.htm

No se han podido verificar ni descargar desde el alojamiento fuente los recursos multimedia y dependencias durante esta publicación. Por tanto, este repositorio conserva el HTML, pero **todavía no es una copia autónoma ni se garantiza que el tour cargue**.

## GitHub Pages

Cuando se incorporen todos los recursos, se podrá habilitar en **Settings → Pages**, seleccionando la rama `main` y la carpeta `/(root)`.

Se conserva el HTML original de 3DVista sin reconstruir ni sustituir su contenido.
