# Auditoría de recuperación 3DVista — 2026-11-23

## Alcance y fuentes examinadas

- `tour.zip`: paquete original parcial.
- `recursos_recuperados_completo.zip`: paquete de recursos recuperados.
- `resultado3.txt` dentro de `tour.zip`: configuración del player utilizada para contrastar las cuadrículas.
- Árbol de la rama `main` del repositorio al inicio de esta auditoría.
- `index.html` actual de GitHub y `README.md` / `.github/workflows/pages.yml`.

No se recibió en esta sesión el archivo `3dvista_recursos_detectados.json` de DevTools ni el directorio completo de Kali. Por ello, este informe describe únicamente lo que se pudo verificar en los archivos entregados y en GitHub.

## 1. Inventario de archivos

| Medición | Resultado |
|---|---:|
| Entradas inventariadas entre ambos ZIP | 972 |
| Entradas del paquete de recursos | 952 |
| Entradas de `tour.zip` | 20 |
| Grupos duplicados por SHA-256 entre rutas | 9 |
| JPG del paquete de recursos que pasaron lectura Pillow | 948 |

La validación JPEG comprueba que Pillow puede abrir y leer los archivos examinados. No certifica que cada mosaico sea el correcto para el recorrido, que no falten mosaicos ni que el contenido visual esté completo.

Se generaron inventarios CSV y JSON fuera del repositorio de GitHub. Deben conservarse como artefactos de auditoría; no se agregaron al repositorio en este commit porque el detalle de rutas internas de los paquetes no es necesario para el resumen operativo.

## 2. Panoramas y mosaicos

La configuración `resultado3.txt` declara:

| Medición | Resultado |
|---|---:|
| Panoramas configurados | 14 |
| Grupos de cara/nivel | 198 |
| Coordenadas de mosaicos esperadas | 6.408 |
| Coordenadas encontradas en el ZIP de recursos | 859 |
| Coordenadas no encontradas en ese ZIP | 5.549 |

Las coordenadas ausentes se calculan comparando las cuadrículas declaradas en la configuración con las rutas presentes en `recursos_recuperados_completo.zip`. **No** significan que el servidor ya no disponga de esos archivos, ni que cada mosaico se necesite en la primera pantalla. Tampoco deben confundirse con los 5.409 errores del descargador antiguo: aquel generaba combinaciones de URL que no necesariamente correspondían a recursos reales.

Se conserva un informe granular local:

- `auditoria_mosaicos_3dvista.csv`
- `auditoria_mosaicos_3dvista.json`

No se agregaron aquí todos los informes granulares para evitar duplicar artefactos de trabajo que se pueden regenerar y revisar por separado.

## 3. Estructura observada en GitHub

Al inicio de esta actualización, la rama `main` contenía:

- `.github/workflows/pages.yml`
- `.nojekyll`
- `README.md`
- `index.html`
- `tools/prepare_pages.py`

No existía la carpeta `site/`. Tampoco estaban presentes en el árbol del repositorio las carpetas `lib/`, `locale/` o `media/`, ni los scripts runtime separados.

El workflow verifica `site/index.html` y `site/lib/tdvplayer.js` antes de desplegar. La última ejecución revisada falló en la comprobación de la carpeta `site/`; no se debe modificar el workflow para publicar un placeholder.

## 4. HTML y dependencias

El HTML del repositorio mide aproximadamente 110 KB. El HTML original de `tour.zip` mide 14.320 bytes; el archivo guardado como `recursos_recuperados/null` mide 14.345 bytes y también es HTML con título “Dual Viewers”.

El HTML del repositorio referencia localmente:

- `lib/tdvplayer.js`
- `script.js`
- `script_general.js`
- `locale/es.txt`
- `lib/WebVRPolyfill.js`
- `lib/Hls.js`
- rutas `media/panorama_...`
- `socialThumbnail.jpg`

No se reemplazó el HTML de GitHub ni se renombró `null`. Hace falta comparar íntegramente las tres variantes, rastrear el origen del archivo `null` y comprobar las dependencias antes de escoger el HTML definitivo.

## 5. Incidencias abiertas

- `recursos_recuperados/null`: archivo HTML de 14.345 bytes; URL de origen no confirmada.
- Descarga HTTP 500 de `media/panorama_2B690725_27DF_A812_41B7_AB9C91E3FC8A_0/f/0/1_1.jpg`; debe reintentarse y contrastarse con solicitudes reales.
- Los IDs `513732A9` y `2B690725` aparecen en la configuración/referencias revisadas, pero no se encontró una carpeta correspondiente a ambos en el ZIP de recursos. No se puede concluir que falten del directorio Kali.
- Falta `3dvista_recursos_detectados.json`, necesario para relacionar las URL observadas en DevTools con los archivos recuperados.
- Faltan pruebas de ejecución local del recorrido completo y validación de medios, navegación, audio/vídeo y dependencias.

## 6. Decisiones de esta actualización de GitHub

- Se actualiza la documentación de estado y se incorpora este informe.
- No se modifica `index.html`, `tools/prepare_pages.py` ni el workflow.
- No se crea `site/` de forma artificial.
- No se suben los ZIP de 88 MB ni recursos multimedia sin completar la auditoría de integridad y derechos.
- No se eliminan, renombran ni sustituyen recursos.

## 7. Próximas tareas técnicas

1. Obtener `3dvista_recursos_detectados.json` y el informe de descarga selectiva.
2. Comparar el HTML del repositorio con las dos variantes del paquete y extraer sus referencias reales.
3. Auditar `script.js`, `script_general.js` y la configuración para identificar todas las rutas requeridas.
4. Validar las cuadrículas contra la configuración y las URL observadas; distinguir mosaicos realmente solicitados de coordenadas teóricas.
5. Reintentar únicamente las URL confirmadas y conservar códigos HTTP, tamaños y hashes.
6. Construir `site/` desde la fuente verificada, ejecutar pruebas locales y revisar solicitudes fallidas.
7. Publicar en GitHub Pages solo después de que el recorrido funcione localmente y los recursos estén autorizados para su distribución.
