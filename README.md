# Línea base de contaminación atmosférica por dióxido de nitrógeno y metano en el área metropolitana de Guatemala (2018-2025) mediante datos satelitales Sentinel-5P

## Descripción
Este proyecto establece una línea base espacial y temporal de la densidad de columna troposférica de dióxido de nitrógeno (NO₂) y de la fracción molar de metano en la columna atmosférica total (CH₄) en el área de estudio, delimitada por los 17 municipios del departamento de Guatemala. El periodo analizado comprende julio de 2018 a junio de 2025. Mediante observaciones de Sentinel-5P/TROPOMI y componentes mensuales del viento de ERA5, se construyen cubos de datos para caracterizar la distribución de los contaminantes, identificar zonas con valores elevados y explorar asociaciones con el corredor CA-9 Sur, los vertederos de zona 3 y AMSA y la circulación del viento. La cobertura efectiva de CH₄ comprende 21 meses. 

Todo el flujo de extracción, procesamiento y análisis fue desarrollado e implementado directamente dentro del entorno en la nube de **JupyterLab en Copernicus Data Space Ecosystem (CDSE)**, eliminando la necesidad de configurar entornos virtuales locales o descargar cientos de matrices intermedias fuera de la infraestructura de Copernicus. El repositorio contiene el código fuente limpio y modularizado, los cubos de datos consolidados (`src/datos/cubos/`), las líneas base generadas (`src/datos/LB/`) y un tablero interactivo complementario para la exploración de NO2.

## Tecnologías Utilizadas
* **Entorno de Ejecución en la Nube:** JupyterLab en Copernicus Data Space Ecosystem (CDSE), kernel `Sentinel Hub` (Python 3.10+)
* **Procesamiento Geoespacial y Cubos de Datos:** `xarray`, `rioxarray`, `geopandas`, `shapely`, `rasterio`, `netCDF4`
* **Análisis Numérico y Estadístico:** `numpy`, `pandas`, `scipy`
* **Visualización y Tablero Interactivo:** `matplotlib`, `seaborn`, `plotly`, `folium`, `streamlit`
* **APIs y Fuentes Satelitales:** Copernicus Data Space Ecosystem (`sentinelhub`, `pystac-client` / STAC API), Copernicus Climate Data Store (`cdsapi` - ERA5)
* **SIG de Escritorio:** QGIS (`compCh4.qgz`)

## Requisitos Previos (Software Necesario)
Para reproducir el proyecto siguiendo la arquitectura original en la nube, únicamente se requiere:
* **Navegador web moderno** (Chrome, Firefox, Edge o Safari) con acceso a internet.
* **Cuenta gratuita en [Copernicus Data Space Ecosystem (CDSE)](https://dataspace.copernicus.eu/)** para acceder al servicio de **JupyterLab** y al kernel preconfigurado (`Sentinel Hub` / Python 3.10+). No se requiere instalación local de Python ni creación de entornos virtuales (`venv` o `conda`) fuera de esta plataforma.
* **Credenciales de API (únicamente para la Trayectoria B — re-extracción desde fuentes originales):**
  * Credenciales OAuth de **Sentinel Hub** (`SH_CLIENT_ID` y `SH_CLIENT_SECRET`) generadas desde el panel de usuario de CDSE.
  * Cuenta gratuita y llave de API en **[Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/)** para la descarga de datos meteorológicos de viento ERA5.

## Instalación Paso a Paso

### 1. Acceso al entorno en la nube (CDSE JupyterLab)
1. Inicia sesión en [Copernicus Data Space Ecosystem (CDSE)](https://dataspace.copernicus.eu/) y abre la herramienta **JupyterLab** desde el menú de aplicaciones (JupyterHub).
2. Selecciona un servidor con recursos estándar (CPU/RAM) y asegúrate de abrir una terminal o notebook utilizando el kernel **`Sentinel Hub`** (que ya incluye de fábrica el ecosistema base geoespacial y científico de Python).

### 2. Clonar el repositorio dentro de `mystorage`
Para conservar tus archivos entre sesiones dentro de CDSE, abre una terminal en JupyterLab, ubícate en el directorio persistente `mystorage` y clona este repositorio:
```bash
cd ~/mystorage
git clone https://github.com/Giosantos23/2026-22523-santos-hernandez-giovanni-alejandro.git
cd 2026-22523-santos-hernandez-giovanni-alejandro
```
### 3. Instalar dependencias complementarias en el kernel activo

El kernel **Sentinel Hub** de CDSE provee nativamente `sentinelhub`, `numpy`, `pandas`, `matplotlib` y herramientas geoespaciales base. Para garantizar que todas las bibliotecas de cubos multidimensionales y visualización estén disponibles en una sesión limpia, ejecuta en una celda inicial del notebook o en la terminal del mismo kernel:

```bash
pip install --quiet xarray==2024.7.0 rioxarray==0.17.0 geopandas==1.0.1 scipy==1.14.1 seaborn==0.13.2 netCDF4==1.7.1 cdsapi==0.7.2
```

> **Nota:** Si se desea ejecutar localmente el tablero interactivo de visualización de NO₂ fuera de CDSE, instalar adicionalmente `streamlit` y `plotly` mediante:
>
> ```bash
> pip install -r src/dashboard_no2/requirements.txt
> ```

---

## Instalación Reproducible

Para garantizar la reproducibilidad exacta del entorno de ejecución desde una sesión limpia en JupyterLab de CDSE:

**Kernel requerido:** Sentinel Hub (Python 3.10.x en entorno Linux de CDSE JupyterHub).

**Dependencias y versiones verificadas:**

- `sentinelhub >= 3.10.0` (preinstalado en el kernel de CDSE)
- `xarray == 2024.7.0` y `netCDF4 == 1.7.1` (lectura, escritura y concatenación de cubos NetCDF)
- `rioxarray == 0.17.0`, `geopandas == 1.0.1` y `shapely >= 2.0.0` (recorte espacial con `amg_limites.geojson` y proyección EPSG:4326 / EPSG:32616)
- `scipy == 1.14.1`, `numpy >= 1.26.0` y `pandas >= 2.2.0` (estadística no paramétrica, correlaciones y series temporales)
- `cdsapi == 0.7.2` (conexión con Copernicus Climate Data Store para ERA5)

**Gestión de credenciales sin exposición en el repositorio:**

El archivo `src/.env.example` documenta las variables requeridas (`SH_CLIENT_ID`, `SH_CLIENT_SECRET`, `CDS_API_URL`, `CDS_API_KEY`). Ninguna credencial real ni archivo temporal se almacena en el repositorio.

---

## Instrucciones de Ejecución

El repositorio está diseñado para reproducirse mediante dos trayectorias según el objetivo del usuario:

### Trayectoria A: Reproducir el análisis con los datos procesados incluidos (Recomendada)

El repositorio ya incluye los cubos de datos finales (`src/datos/cubos/`) y las líneas base consolidadas (`src/datos/LB/`), evitando descargar nuevamente las matrices crudas mensuales. Esta trayectoria **no requiere configurar credenciales de API**.

1. Abre JupyterLab en CDSE, entra a la carpeta del proyecto dentro de `mystorage` y verifica que esté activo el kernel **Sentinel Hub**.
2. Ejecuta los notebooks de análisis final en el siguiente orden:

   **Análisis de Dióxido de Nitrógeno (NO₂):**
   - Abrir y ejecutar `src/no2/AnálisisFinalNO2.ipynb`.
   - **Entradas:** `src/datos/cubos/Cubo_NO2_Final.nc`, `src/datos/LB/Linea_Base_NO2_AMG.nc`, `src/datos/cubos/Cubo_Viento_AMG_Final.nc` y `src/limits/amg_limites.geojson`.
   - **Salidas:** Estadísticos descriptivos metropolitanos, análisis de proximidad en el corredor CA-9 Sur, series temporales, correlaciones con viento ERA5 y figuras de resultados.

   **Análisis de Metano (CH₄):**
   - Abrir y ejecutar `src/ch4/AnalisisFinalCH4.ipynb`.
   - **Entradas:** `src/datos/cubos/Cubo_CH4_Final.nc`, `src/datos/LB/Linea_Base_CH4_AMG.nc`, `src/datos/cubos/Cubo_Viento_AMG_Final.nc` y `src/limits/amg_limites.geojson`.
   - **Salidas:** Serie temporal de cobertura efectiva (21 meses), evaluación de buffers espaciales alrededor de los vertederos de Zona 3 y AMSA, y métricas estadísticas.

   **Exploración 3D y Comparativa Regional (Opcional):**
   - Ejecutar `src/no2/pruebas_3D_NO2.ipynb` para visualizaciones tridimensionales.
   - Ejecutar `python src/comparison/comppaises.py` utilizando `src/comparison/TROPOMI_GHSSMOD_ANNUAL1.csv` para la comparativa regional.

### Trayectoria B: Repetir el procesamiento completo desde las fuentes satelitales

Si se desea reconstruir las matrices mensuales y los cubos desde cero consultando los servidores de Copernicus:

**1. Configurar credenciales en CDSE JupyterLab**

- Copia la plantilla de variables de entorno:

  ```bash
  cp src/.env.example src/.env
  ```

- Completa `SH_CLIENT_ID` y `SH_CLIENT_SECRET` en `src/.env` (o mediante `SHConfig()` en Python) para Sentinel Hub.
- Para ERA5 (CDS), crea el archivo `/home/jovyan/.cdsapirc` con tu URL y llave personal (`UID:API_KEY`).

**2. Ejecutar el flujo secuencial de extracción y construcción de cubos**

- **Paso 1 — Delimitación geográfica (`src/limits/`):**
  - `extraerGTMunicipios.py` filtra los 17 municipios del departamento de Guatemala a partir de `gtm_admin2.geojson` y genera `amg_limites.geojson`.

- **Paso 2 — Flujo de Dióxido de Nitrógeno (`src/no2/`):**
  - `extractNO2.ipynb`: Consulta Sentinel-5P L2 (`qa_value > 0.75`) vía Process API y guarda las matrices mensuales NetCDF.
  - `BuildNO2DataCube.ipynb`: Ensambla las matrices mensuales en `src/datos/cubos/Cubo_NO2_Final.nc` y calcula `src/datos/LB/Linea_Base_NO2_AMG.nc`.
  - `AnálisisFinalNO2.ipynb`: Ejecuta el análisis estadístico y espacial final.

- **Paso 3 — Flujo de Metano (`src/ch4/`):**
  - `extractCH4.ipynb`: Consulta Sentinel-5P L2 CH₄ (`qa_value > 0.50`) y descarga los meses con cobertura válida.
  - `BuildCH4DataCube.ipynb`: Construye `src/datos/cubos/Cubo_CH4_Final.nc` y `src/datos/LB/Linea_Base_CH4_AMG.nc`.
  - `AnalisisFinalCH4.ipynb`: Ejecuta el análisis final de metano.

- **Paso 4 — Flujo Meteorológico de Viento (`src/viento/`):**
  - `buildERA5Cube.ipynb`: Descarga componentes `u10` y `v10` de ERA5 vía `cdsapi`, calcula magnitud vectorial y genera `src/datos/cubos/Cubo_Viento_AMG_Final.nc` y `src/datos/LB/Linea_Base_Viento_AMG.nc`.

---

## Ejecución del Tablero Interactivo de NO₂ (Complementario)

Para lanzar la aplicación visual de exploración de NO₂:

```bash
streamlit run src/dashboard_no2/app.py
```

---

## Estructura del Repositorio

```text
.
├── capturas/                  # Evidencia visual del entorno, código y resultados (captura-01.png a captura-10.png)
├── demo/                      # Video demostrativo del proyecto en ejecución (demo.mp4)
├── docs/                      # Informe final de graduación y consentimiento firmado en PDF
├── src/
│   ├── ch4/                   # Extracción, construcción de cubo y análisis de metano (CH4)
│   ├── comparison/            # Script y datos de comparativa regional
│   ├── dashboard_no2/         # Aplicación web interactiva en Streamlit para NO2
│   ├── datos/
│   │   ├── cubos/             # Cubos de datos NetCDF consolidados (NO2, CH4 y Viento ERA5)
│   │   └── LB/                # Líneas base espaciales consolidadas en NetCDF
│   ├── limits/                # Polígonos vectoriales del Área Metropolitana de Guatemala (GeoJSON)
│   ├── no2/                   # Extracción, construcción de cubo y análisis de dióxido de nitrógeno (NO2)
│   ├── viento/                # Extracción y construcción del cubo meteorológico ERA5
│   └── .env.example           # Plantilla de variables de entorno (sin credenciales reales)
└── README.md
```

---

## Capturas

Las capturas de pantalla que evidencian el entorno en JupyterLab, el procesamiento de los cubos NetCDF y los resultados principales del análisis se encuentran en la carpeta [`/capturas`](./capturas):

- `captura-01.png` – `captura-05.png`: Configuración del entorno en CDSE JupyterLab, extracción con filtros de calidad (`qa_value`), ensamblaje de cubos NetCDF y series temporales de NO₂ y CH₄.
- `captura-06.png` – `captura-10.png`: Identificación espacial de hotspots (corredor CA-9 Sur, vertederos de Zona 3 y AMSA), acoplamiento con campos de viento ERA5 y visualización en el tablero interactivo.

---

## Demo

El video demostrativo del proyecto (introducción, recorrido por el entorno de JupyterLab, ejecución de los módulos de análisis y presentación de resultados) está disponible en [`/demo/demo.mp4`](./demo/demo.mp4).

---

## Documentación

- **Informe Final de Graduación:** [`/docs/informe_final.pdf`](./docs/informe_final.pdf)
- **Consentimiento de Uso de Foto y Video (Firmado):** [`/docs/consentimiento_firmado.pdf`](./docs/consentimiento_firmado.pdf)

---

## Autor

**Giovanni Alejandro Santos Hernández** – Carné 22523

---

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

MIT License

Copyright (c) 2026 Giovanni Alejandro Santos Hernández

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.