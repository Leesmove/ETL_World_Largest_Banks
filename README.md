# 🌍 World's Largest Banks – ETL Project

Este proyecto aplica el proceso de **ETL (Extracción, Transformación y Carga)** a una tabla web con información sobre los **10 bancos más grandes del mundo por capitalización de mercado**. Basado en un laboratorio práctico del curso "Python Project for Data Engineering", impartido por IBM a través de Coursera y desarrollado por Skills Network Labs.

He adaptado y documentado el flujo ETL para consolidar mis habilidades como analista de datos junior y compartirlo como parte de mi portafolio profesional.

## 📌 Objetivo
El objetivo es **automatizar el flujo de datos** desde una fuente web hasta su almacenamiento final en una base de datos local. Es parte de mi portafolio como analista de datos en formación.

---

## 🔧 Herramientas y librerías utilizadas

- **Python** 🐍
- `requests` y `BeautifulSoup` – para la **extracción de datos web (web scraping)**
- `pandas` y `numpy` – para la **transformación y limpieza de datos**
- `sqlite3` – para la **carga en una base de datos SQLite**
- **VS Code** y **GitHub Desktop** – para el desarrollo y control de versiones

---

## 📊 Datos procesados

La información fue extraída desde una tabla en la web (Wikipedia) y transformada de la siguiente forma:

- Se eliminaron columnas innecesarias
- Se convirtieron los valores de capitalización a dólares estadounidenses
- Se generaron archivos `.csv` y una base de datos `.db` como resultado final

---

## 📁 Archivos principales

| Archivo | Descripción |
|--------|-------------|
| `banks_project.py` | Script principal del proceso ETL |
| `Largest_banks_data.csv` | Datos originales extraídos de la web |
| `exchange_rate.csv` | Tasas de cambio usadas para la conversión |
| `Banks.db` | Base de datos SQLite con la tabla final |
| `code_log.txt` | Registro de pasos y decisiones tomadas en el código |
| `.gitignore` | Configuración para excluir archivos innecesarios (por ejemplo, entorno virtual `env/`) |

---

## 🚀 Cómo ejecutar el proyecto

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/ETL_World_Largest_Banks.git
