# Auditoría de recuperación 3DVista — 2026-11-23

## Alcance

Se revisaron `tour.zip`, `recursos_recuperados_completo.zip`, los archivos de configuración/scripts incluidos y el árbol de GitHub `main`. No se recibió todavía `3dvista_recursos_detectados.json` de DevTools ni el directorio completo de Kali.

## 1. HTML de entrada: comparación y decisión

Se compararon tres variantes:

| Variante | Tamaño aproximado | Observación |
|---|---:|---|
| `index.html` del repositorio antes de esta actualización | 110 KB | Captura con DOM del visor ya renderizado y elementos de interfaz añadidos; no se usa como fuente limpia |
| HTML dentro de `tour.zip` | 14.320 bytes | Fuente original capturada, pero contiene `%3Fv=` en varias rutas de recursos |
| `recursos_recuperados/null` | 14.345 bytes | Variante normalizada del HTML, con `?v=` en las rutas y URL absoluta para la miniatura social |

La variante `null` conserva la estructura del HTML fuente y corrige la codificación de las query strings. Para el sitio GitHub Pages se ajustó la ruta de `socialThumbnail.jpg` a una ruta local relativa, porque el script de preparación coloca esa imagen en la raíz del sitio.

**Decisión aplicada:** se restauró `index.html` en la raíz con la versión normalizada y se conservó el HTML anterior sin cambios en `archive/index_github_snapshot_2026-11-23.html`. No se eliminó ningún archivo.

El HTML continúa apuntando a `https://cloud.3dvista.com/tdvanalytics.js` para analítica, como en la fuente. Esa llamada externa no equivale a que los medios del tour estén completos.

## 2. Scripts y runtime

- `script.js`: 148.325 bytes en ambas rutas del ZIP; SHA-256 idéntico.
- `lib/tdvplayer.js`: 3.128.929 bytes en ambas rutas del ZIP; SHA-256 idéntico.
- `script_general.js`: 106.703 bytes; contiene la configuración del recorrido y las referencias a los 14 panoramas.
- `locale/es.txt`: presente.
- `socialThumbnail.jpg`: presente bajo la ruta de hosting del ZIP y normalizable a la raíz del sitio.
- `lib/WebVRPolyfill.js`: referenciado por el HTML, no presente en los ZIP revisados.
- `lib/Hls.js`: referenciado por el HTML, no presente en los ZIP revisados.
- `lib/pdfjs/web/viewer.html`: aparece como ruta de visor PDF en el código genérico de `script.js`; no se halló esa carpeta en los ZIP. No se detectaron referencias a archivos PDF en la configuración del tour revisada, por lo que queda como dependencia condicional.

No se sustituyeron bibliotecas por versiones de otros tours o por descargas de terceros.

## 3. Medios y panoramas

La configuración declara 14 panoramas y 198 grupos cara/nivel. La auditoría de cuadrículas calculó 6.408 coordenadas esperadas. En el paquete de recursos se encontraron 948 JPG:

| Tipo de JPG recuperado | Cantidad |
|---|---:|
| Mosaicos de cuadrícula | 859 |
| Imágenes VR | 51 |
| Imágenes VR2gen | 27 |
| Miniaturas panorámicas | 11 |
| **Total** | **948** |

Comparación de mosaicos: 859 presentes y 5.549 coordenadas configuradas ausentes del ZIP. La ausencia en el ZIP no demuestra que el servidor original no las tenga ni que todas se soliciten en la primera vista.

Miniaturas: faltan las miniaturas de estos tres IDs:
- `panorama_513732A9_42C4_7F27_4170_7C03EF83FFC6_t.jpg`
- `panorama_2AC6AEE0_27DF_5812_4197_A8AA1B57A49D_t.jpg`
- `panorama_2B690725_27DF_A812_41B7_AB9C91E3FC8A_t.jpg`

En cuanto a mosaicos, los IDs `513732A9` y `2B690725` no tienen mosaicos en el ZIP de recursos; el ID `2AC6AEE0` tiene seis mosaicos. El paquete original `tour.zip` aporta esos seis mosaicos del ID `2AC6AEE0`, con query string en el nombre que el script de preparación normaliza.

La auditoría granular de coordenadas está disponible en los artefactos locales `auditoria_mosaicos_3dvista.csv` y `auditoria_mosaicos_3dvista.json`.

## 4. Prueba de preparación en staging

Se probó el mapeo de rutas de `tools/prepare_pages.py` contra una estructura combinada de los dos ZIP:

- 956 archivos copiados al staging.
- Aproximadamente 91,9 MB copiados.
- `index.html`, `lib/tdvplayer.js` y `script_general.js` presentes.
- 948 JPG en `media/`.
- `lib/WebVRPolyfill.js`, `lib/Hls.js` y `lib/pdfjs/web/viewer.html` ausentes.

Esto es una prueba de ensamblaje de rutas, no una prueba de ejecución del recorrido en navegador. El staging no se publicó.

## 5. Estado del repositorio y Pages

El workflow exige `site/index.html` y `site/lib/tdvplayer.js`, y despliega `site/`. La carpeta `site/` todavía no está en el repositorio. La actualización de documentación y del HTML raíz no activa el workflow, que está limitado a cambios en `site/**` o en el propio workflow.

No se alteró el workflow para publicar una versión incompleta. No se afirmó que Pages esté funcionando.

## 6. Próximas tareas

1. Obtener `3dvista_recursos_detectados.json` y contrastar las solicitudes reales de DevTools.
2. Comparar las URLs observadas con los 948 JPG recuperados y obtener únicamente los archivos realmente faltantes desde la fuente autorizada.
3. Recuperar las bibliotecas WebVR/HLS desde la distribución autorizada de este tour o del titular del software, verificando versión y licencia.
4. Confirmar si el tour usa PDF, audio, vídeo, modelos 3D u otros recursos condicionales.
5. Ejecutar `tools/prepare_pages.py` con la carpeta fuente completa y verificar el recorrido localmente.
6. Solo entonces incorporar `site/` y ejecutar GitHub Pages.


## Actualización: defecto de la carpeta envolvente

La prueba con la estructura real del ZIP detectó que la versión anterior del preparador no reconocía los archivos runtime bajo la carpeta superior tour/. Se corrigió el mapeo para retirar solo ese primer componente antes de resolver rutas. La prueba posterior produjo 956 archivos y dejó presentes index.html, lib/tdvplayer.js, script.js, script_general.js, locale/es.txt y socialThumbnail.jpg. Se añadieron seis pruebas unitarias para cubrir la estructura con envoltura, la estructura de recursos recuperados y la exclusión de null e informes.
