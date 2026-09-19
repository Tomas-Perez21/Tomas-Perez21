# Job Feed Filter & Data Ingestion Pipeline

Script de automatización en Python diseñado para la ingesta, filtrado multietapa y exportación de ofertas laborales orientadas a perfiles Junior/Trainee en Data Analytics desde la API de RemoteOK.

## 🚀 Funcionalidades Clave

- **Ingesta de datos:** Conexión a la API pública de RemoteOK mediante peticiones HTTP.
- **Filtro de Antigüedad:** Procesamiento exclusivo de avisos publicados en los últimos 7 días.
- **Filtrado Inteligente por Regex:**
  - **Blacklist:** Descarte automático de puestos Senior, Lead, Manager o Architect.
  - **Keywords exactas:** Matcheo de títulos y tecnologías clave (`SQL`, `Python`, `Power BI`, `Excel`, `Pandas`).
- **Mecanismo Anti-duplicados:** Lectura del archivo histórico para evitar reprocesar o duplicar URLs ya guardadas.
- **Persistencia en CSV:** Exportación estructurada compatible de forma nativa con Excel (`delimiter=";"` y `encoding="utf-8-sig"`).

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Bibliotecas:** `requests`, `re` (Regex), `csv`, `datetime`, `os`.

## ⚙️ Cómo Ejecutar el Proyecto

1. Clonar este repositorio:
   ```bash
   git clone [https://github.com/Tomas-Perez21/job-feed-filter.git](https://github.com/Tomas-Perez21/job-feed-filter.git)

2. Acceder a la carpeta del  proyecto:
    cd job-feed-filter

3. Instalar las dependencias necesarias:
    pip install requests

4. Ejecutar el script principal:
    python busqueda_laboral.py
