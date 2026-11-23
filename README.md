# Recorridos 3D — 3DVista

Repositorio de trabajo para recuperar y publicar el recorrido virtual **Dual Viewers** (3DVista Player v1901).

## Estado real

Este repositorio todavía **no contiene una copia autónoma funcional** del recorrido. El HTML ya está publicado, pero faltan recursos multimedia y dependencias para ejecutarlo desde GitHub Pages.

### Recursos ya identificados en el archivo `tour.zip`

- `index.html` original del recorrido (ubicado en la captura bajo `storage.net-fs.com/hosting/2727323/443/`).
- `script.js` y `script_general.js`.
- `lib/tdvplayer.js`.
- `locale/es.txt`.
- `socialThumbnail.jpg`.
- Seis mosaicos de nivel 1 del panorama `2AC6AEE0_27DF_5812_4197_A8AA1B57A49D`.

### Recuperación posterior en Kali

Se descargaron seis mosaicos de nivel 1 adicionales para el panorama:

`2B690725_27DF_A812_41B7_AB9C91E3FC8A`.

Esos archivos están en el equipo Kali del usuario y todavía deben incorporarse al repositorio mediante el paquete actualizado.

### Dependencias y recursos aún por comprobar

- Niveles de resolución y mosaicos restantes de todos los panoramas.
- Miniaturas, imágenes auxiliares, audio, vídeo y demás medios que el recorrido solicite dinámicamente.
- `lib/WebVRPolyfill.js` y `lib/Hls.js`, referenciados por el HTML.
- Recursos adicionales como cursores y archivos externos.
- Carga y funcionamiento real en navegador mediante GitHub Pages.

## Preparar los archivos para publicación

El script `tools/prepare_pages.py` permite construir una carpeta `site/` desde el directorio local `tour/`. Conserva las rutas relativas del proyecto, combina los recursos recuperados y elimina el sufijo de consulta que algunas descargas guardan literalmente en el nombre del archivo (por ejemplo `?v=...`).

En Kali:

```bash
python3 tools/prepare_pages.py --source ~/tour --output ./site
```

Después de preparar `site/`, se debe probar con un servidor HTTP local antes de publicarlo:

```bash
cd site
python3 -m http.server 8000
```

Abrir `http://localhost:8000/`.

## Fuente

https://storage.net-fs.com/hosting/2727323/443/index.htm

La publicación de los recursos debe respetar los derechos del propietario del recorrido y las licencias de 3DVista y de terceros. Este repositorio no incluye credenciales ni intenta eludir controles de acceso.

## GitHub Pages

No se debe considerar habilitada ni validada la publicación del recorrido hasta que se incorporen los recursos, se pruebe localmente y se confirme la configuración de Pages.
