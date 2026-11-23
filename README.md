# Recorridos 3D — 3DVista

Repositorio de trabajo para recuperar, auditar y preparar una copia autónoma del recorrido virtual **Dual Viewers** (3DVista Player v1901).

## Estado real (auditoría 2026-11-23)

**La copia autónoma todavía no está lista para publicación.** No existe la carpeta `site/` y el workflow de GitHub Pages no ha podido desplegar el recorrido. El workflow requiere `site/index.html` y `site/lib/tdvplayer.js`; no se debe crear un sitio vacío para superar esa comprobación.

La auditoría se realizó sobre los ZIP adjuntos `tour.zip` y `recursos_recuperados_completo.zip`, además del árbol actual de este repositorio. Los resultados completos y sus limitaciones están en [docs/AUDITORIA_RECUPERACION_2026-11-23.md](docs/AUDITORIA_RECUPERACION_2026-11-23.md).

### Evidencia disponible

- Se inventariaron **972 entradas** entre los dos ZIP: 952 en el paquete de recursos y 20 en `tour.zip` (el total de entradas del ZIP puede incluir directorios).
- Se detectaron **9 grupos de duplicados por SHA-256** entre rutas de ambos paquetes.
- Se validó la lectura JPEG de **948 archivos JPG** del paquete de recursos; esto valida que se pueden leer como JPEG, no que el recorrido esté completo.
- La configuración del player en `resultado3.txt` declara **14 panoramas**, **198 grupos cara/nivel** y **6.408 coordenadas de mosaicos**.
- En el ZIP de recursos se localizaron **859 mosaicos** correspondientes a esas cuadrículas; **5.549 coordenadas configuradas no están presentes en ese ZIP**. Esto no demuestra que el servidor no las tenga ni que todas se soliciten en la primera vista.
- El repositorio contiene actualmente `index.html`, `README.md`, `.nojekyll`, el workflow y `tools/prepare_pages.py`. Todavía no contiene `site/`, los scripts runtime ni los medios requeridos en las rutas del recorrido.

### Recursos y dependencias identificados

El HTML del recorrido referencia, entre otros:

- `script.js` y `script_general.js`
- `lib/tdvplayer.js`
- `lib/WebVRPolyfill.js` y `lib/Hls.js`
- `locale/es.txt`
- Recursos bajo `media/`, incluidos mosaicos de panoramas
- `socialThumbnail.jpg`

La presencia de una referencia en HTML no confirma que el archivo esté recuperado.

### Incidencias que siguen abiertas

1. El archivo `recursos_recuperados/null` del paquete mide 14.345 bytes y contiene HTML titulado “Dual Viewers”. Su URL y nombre de origen todavía deben verificarse; no se renombra ni elimina.
2. El informe de descarga selectiva registró un HTTP 500 para `media/panorama_2B690725_27DF_A812_41B7_AB9C91E3FC8A_0/f/0/1_1.jpg`. Debe reintentarse de forma controlada y contrastarse con las solicitudes reales.
3. Los identificadores `513732A9` y `2B690725` aparecen en las referencias/configuración revisadas, pero no se encontró una carpeta correspondiente a ambos en el ZIP de recursos proporcionado. No se concluye que no existan en el equipo de trabajo.
4. El HTML del repositorio (aprox. 110 KB) difiere en tamaño del HTML original incluido en `tour.zip` (14.320 bytes) y del HTML guardado como `recursos_recuperados/null` (14.345 bytes). No se reemplazó ninguno; hay que comparar su contenido y procedencia antes de decidir cuál debe ser el punto de entrada.
5. Falta el archivo `3dvista_recursos_detectados.json` generado desde DevTools para contrastar las URL realmente observadas con los archivos locales.

## Preparación y validación

El script `tools/prepare_pages.py` prepara `site/` desde una carpeta fuente local, conservando rutas relativas y normalizando nombres con sufijos de consulta. Antes de ejecutarlo, la carpeta fuente debe contener la estructura completa verificada.

Cuando la recuperación esté completa:

```bash
python3 tools/prepare_pages.py --source ~/tour --output ./site
cd site
python3 -m http.server 8000
```

Probar el recorrido en navegador y corregir todas las solicitudes fallidas antes de publicar. Después, incorporar `site/` y ejecutar el workflow de Pages.

## Fuente y derechos

Recorrido de referencia: https://storage.net-fs.com/hosting/2727323/443/index.htm

La publicación debe respetar los derechos del propietario del recorrido y las licencias de 3DVista y de terceros. Este repositorio no debe distribuir recursos sin autorización.

## GitHub Pages

El workflow está preparado para publicar únicamente `site/`. La publicación no se considera habilitada ni validada hasta que se incorporen los recursos necesarios, se pruebe localmente y se confirme una ejecución satisfactoria de GitHub Actions.
