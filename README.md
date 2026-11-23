# Recorridos 3D — 3DVista

Repositorio de recuperación y preparación del recorrido virtual **Dual Viewers** (3DVista Player v1901).

## Estado real — auditoría 2026-11-23

**Todavía no es una copia autónoma lista para publicar.** La carpeta `site/` no existe y el workflow de GitHub Pages requiere `site/index.html` y `site/lib/tdvplayer.js`. No se debe desplegar un placeholder ni declarar el recorrido funcional sin probar los medios.

El HTML de la raíz se ha restaurado a partir del HTML fuente del paquete original y de su variante normalizada recuperada. La versión previa de 110 KB se conserva como respaldo en `archive/index_github_snapshot_2026-11-23.html`.

## Hallazgos verificados

- Inventario combinado de los ZIP: 972 entradas.
- 948 imágenes JPG recuperadas y legibles.
- De esas imágenes: **859 mosaicos**, **78 imágenes VR/VR2gen** y **11 miniaturas**.
- Configuración: **14 panoramas**, **198 grupos cara/nivel** y **6.408 coordenadas de mosaicos**.
- Comparación de cuadrículas: 859 mosaicos presentes y 5.549 coordenadas no encontradas en el ZIP de recursos.
- Solo 11 de las 14 miniaturas panorámicas están presentes.
- Los archivos `script.js` y `lib/tdvplayer.js` duplicados en las dos rutas del ZIP tienen el mismo SHA-256.
- Una prueba de preparación con el mapeo del script actual produjo un staging de 958 archivos (aprox. 91,9 MB); esto no certifica que todos los medios necesarios estén presentes.

Detalle y limitaciones: [docs/AUDITORIA_RECUPERACION_2026-11-23.md](docs/AUDITORIA_RECUPERACION_2026-11-23.md).

## Recursos y dependencias

El HTML/configuración requieren, entre otros:

- `script.js`, `script_general.js`, `lib/tdvplayer.js`
- `locale/es.txt`, `socialThumbnail.jpg`
- Recursos de `media/`: mosaicos, variantes VR y miniaturas
- `lib/WebVRPolyfill.js` y `lib/Hls.js` (referenciados por el HTML, no presentes en los ZIP entregados)

El código genérico de `script.js` contiene una ruta para el visor PDF `lib/pdfjs/web/viewer.html`, pero no se encontraron referencias a archivos PDF dentro de la configuración del recorrido examinada. Se considera una dependencia condicional hasta confirmar si el tour utiliza esa función.

## Preparar y probar localmente

El script `tools/prepare_pages.py` construye `site/` desde una carpeta fuente local y conserva las rutas relativas esperadas:

```bash
python3 tools/prepare_pages.py --source ~/tour --output ./site
cd site
python3 -m http.server 8000
```

Abrir `http://localhost:8000/` y revisar la consola/red del navegador. Antes de publicar, completar dependencias y medios, corregir solicitudes fallidas y comprobar navegación, panoramas, audio/vídeo y funciones especiales.

## GitHub Pages

El workflow publica únicamente `site/`. No se ha cambiado para aceptar una carpeta incompleta. La actualización documental de esta fase no activa el workflow porque no modifica `site/**`.

## Fuente y derechos

Recorrido de referencia: https://storage.net-fs.com/hosting/2727323/443/index.htm

La distribución debe respetar los derechos del propietario del recorrido y las licencias de 3DVista y terceros. No se incorporan recursos externos de otros tours como sustitutos.


## Compatibilidad del preparador

El preparador ahora acepta la estructura extraída del ZIP con una carpeta superior llamada tour, además de fuentes que ya tengan los archivos en la raíz. Se añadieron pruebas unitarias para ambas rutas y para excluir archivos de auditoría o el recurso sin nombre.
