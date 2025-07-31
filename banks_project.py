# 📦 1. Importamos las librerías necesarias
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

# 📘 2. Función para registrar el progreso en un archivo de texto
def log_progress(message):
    with open("code_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} : {message}\n")

# 🧪 3. Función para extraer datos de la página web
def extract(url, table_attribs):
    print("🔍 Buscando tablas con encabezados:")

    # Obtenemos el contenido de la página
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    tables = soup.find_all("table")

    # Mostramos los encabezados de cada tabla
    for i, table in enumerate(tables):
        try:
            df_test = pd.read_html(str(table))[0]
            print(f"Tabla {i}: {list(df_test.columns)}")
        except:
            continue

    # Elegimos la tabla correcta (la número 0 con capitalización de mercado)
    df = pd.read_html(str(tables[0]))[0]

    # Renombramos columnas para simplificar
    df = df.rename(columns={
        "Bank name": "Name",
        "Market cap (US$ billion)": "MC_USD_Billion"
    })

    # Seleccionamos solo las columnas deseadas
    df = df[["Name", "MC_USD_Billion"]].copy()

    # Limpiamos la columna numérica por si tiene saltos de línea o símbolos
    df["MC_USD_Billion"] = df["MC_USD_Billion"].replace('[\n]', '', regex=True)
    df["MC_USD_Billion"] = df["MC_USD_Billion"].astype(float)

    return df

# 🔧 4. Función para transformar los datos usando tasas de cambio
def transform(df, csv_path):
    exchange_df = pd.read_csv(csv_path)
    exchange_rate = exchange_df.set_index('Currency').to_dict()['Rate']
    df['MC_GBP_Billion'] = [np.round(x * exchange_rate['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_rate['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_rate['INR'], 2) for x in df['MC_USD_Billion']]
    return df

# 💾 5. Función para guardar como archivo CSV
def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)

# 🛢️ 6. Función para guardar en una base de datos SQLite
def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists="replace", index=False)

# 🔍 7. Función para ejecutar consultas SQL
def run_query(query_statement, sql_connection):
    result = pd.read_sql(query_statement, sql_connection)
    print(f"\n📥 Consulta:\n{query_statement}")
    print(result)

# 🚀 8. Programa principal
if __name__ == "__main__":
    # Variables de configuración
    url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
    csv_path = "exchange_rate.csv"
    table_attribs = ["Name", "MC_USD_Billion"]
    output_csv = "./Largest_banks_data.csv"
    db_name = "Banks.db"
    table_name = "Largest_banks"

    log_progress("🔄 Preliminares completos. Iniciando proceso ETL")

    # Extraemos los datos
    df = extract(url, table_attribs)
    log_progress("✅ Datos extraídos. Iniciando transformación")

    # Transformamos los datos con tasas de cambio
    df = transform(df, csv_path)
    log_progress("✅ Transformación completa. Guardando resultados")

    # Guardamos como CSV
    load_to_csv(df, output_csv)
    log_progress("📁 Datos guardados como CSV")

    # Conectamos con base de datos
    conn = sqlite3.connect(db_name)
    log_progress("🔌 Conexión a base de datos establecida")

    # Guardamos en la base de datos
    load_to_db(df, conn, table_name)
    log_progress("🗃️ Datos cargados en tabla de base de datos")

    # Ejecutamos consultas
    run_query("SELECT * FROM Largest_banks", conn)
    run_query("SELECT AVG(MC_GBP_Billion) AS Promedio_GBP FROM Largest_banks", conn)
    run_query("SELECT Name FROM Largest_banks LIMIT 5", conn)
    log_progress("📊 Consultas ejecutadas correctamente")

    # Cerramos conexión
    conn.close()
    log_progress("✅ Conexión cerrada. Proceso completado.")
