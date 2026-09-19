import csv
from datetime import datetime, timedelta, timezone
import os
import re
import feedparser
import requests

ARCHIVO_CSV = "avisos_filtrados.csv"

DIAS_LIMITE = 7
FECHA_LIMITE = datetime.now(timezone.utc) - timedelta(days=DIAS_LIMITE)

KEYWORDS_TITULO = [
    "data",
    "analyst",
    "analista",
    "bi",
    "operations",
    "operaciones",
    "reporting",
    "analytics",
]
KEYWORDS_TECH = ["sql", "python", "power bi", "excel", "pandas"]
BLACKLIST = [
    "senior",
    "sr",
    "lead",
    "principal",
    "manager",
    "gerente",
    "architect",
    "head",
]

URL_PRUEBA_API = "https://remoteok.com/api"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def obtener_urls_procesadas(nombre_archivo=ARCHIVO_CSV):
    """Lee el CSV existente para evitar procesar o guardar avisos repetidos."""
    urls_existentes = set()
    if os.path.exists(nombre_archivo):
        with open(
            nombre_archivo, mode="r", encoding="utf-8-sig"
        ) as archivo:
           
            reader = csv.reader(archivo, delimiter=";")
            for fila in reader:
                if len(fila) >= 5:
                    urls_existentes.add(
                        fila[4]
                    ) 
    return urls_existentes


def guardar_en_csv(avisos, nombre_archivo=ARCHIVO_CSV):
    if not avisos:
        print("No se encontraron avisos nuevos para exportar.")
        return

    encabezados = [
        "Fecha_de_Extraccion",
        "Etiqueta",
        "Puesto",
        "Compañia",
        "URL",
    ]
    with open(
            nombre_archivo, mode="a", newline="", encoding="utf-8-sig"
        ) as archivo:
            writer = csv.writer(archivo, delimiter=";")
    
           
            if archivo.tell() == 0:
                writer.writerow(encabezados)
    
            for aviso in avisos:
                writer.writerow(
                    [
                        datetime.now().strftime("%Y-%m-%d"),
                        aviso["etiqueta"],
                        aviso["puesto"],
                        aviso["compania"],
                        aviso["url"],
                    ]
                )
    
    print(
            f"\n✅ Proceso finalizado: Se guardaron {len(avisos)} avisos nuevos en '{nombre_archivo}'."
        )

def procesar_y_filtrar_avisos(trabajos):
    urls_guardadas = obtener_urls_procesadas()
    avisos_para_guardar = []

    for job in trabajos:
        titulo = job.get("position", "").lower()
        descripcion = job.get("description", "").lower()
        link = job.get("url", "")
        fecha_raw = job.get("date", "")

        if not titulo or not link:
            continue

        if link in urls_guardadas:
            continue

        if fecha_raw:
            try:
                fecha_dt = datetime.fromisoformat(
                    fecha_raw.replace("Z", "+00:00")
                )
                if fecha_dt < FECHA_LIMITE:
                    continue
            except Exception:
                pass

        if any(
            re.search(rf"\b{re.escape(palabra)}\b", titulo)
            for palabra in BLACKLIST
        ):
            continue

        coincide_titulo = any(
            re.search(rf"\b{re.escape(palabra)}\b", titulo)
            for palabra in KEYWORDS_TITULO
        )
        coincide_tech = any(
            re.search(rf"\b{re.escape(palabra)}\b", descripcion)
            for palabra in KEYWORDS_TECH
        )

        if coincide_titulo or coincide_tech:
            es_jr = any(
                re.search(rf"\b{re.escape(j)}\b", titulo)
                for j in ["junior", "jr", "trainee", "entry level", "intern"]
            )

            if coincide_titulo:
                etiqueta = "[MARCADO JR]" if es_jr else "[REVISAR]"
            else:
                etiqueta = "[POSEE TECH REQUERIDA]"

            print(f"{etiqueta} Puesto: {job.get('position')}")
            print(f"Compañía: {job.get('company')}")
            print(f"URL: {link}")
            print("-" * 40)

            avisos_para_guardar.append(
                {
                    "etiqueta": etiqueta,
                    "puesto": job.get("position"),
                    "compania": job.get("company"),
                    "url": link,
                }
            )

    guardar_en_csv(avisos_para_guardar)

if __name__ == "__main__":
    print("Conectando a la API de RemoteOK...")

    try:
        response = requests.get(URL_PRUEBA_API, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            datos = response.json()
            lista_trabajos = datos[1:]

            print(
                f"Se obtuvieron {len(lista_trabajos)} avisos crudos. Filtrando...\n"
            )

            procesar_y_filtrar_avisos(lista_trabajos)
        else:
            print(f"Error HTTP al conectar: {response.status_code}")

    except Exception as e:
        print(f"Ocurrió un error en la petición: {e}")    
    