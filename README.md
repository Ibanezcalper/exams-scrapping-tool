# Udemy Exam Scraper / Extractor de Exámenes de Udemy

[English](#english) | [Español](#español)

---

## English

### Overview
This repository contains a robust Python-based automation tool that utilizes Selenium and BeautifulSoup to scrape practice exams from Udemy. Specifically, it was designed to extract questions, multiple-choice options, correct answers, detailed justifications, and embedded images (diagrams) for offline study and backup.

### Key Features
- **Anti-Bot Bypass**: Uses an existing Chrome profile via remote debugging (`--remote-debugging-port`) to bypass Cloudflare and standard bot protections.
- **Full Exam Extraction**: Iterates through entire practice tests automatically.
- **Image Downloading**: Identifies, downloads, and maps embedded images within questions or answers to a local `imagenes_examen` directory.
- **Structured Output**: Compiles all scraped data into a structured JSON format (`examen_completo.json`) for easy parsing and ingestion into other applications.

### Tech Stack
- Python
- Selenium WebDriver
- BeautifulSoup4
- Chrome Remote Debugging

### Repository Structure
- **`scraper.py`**: The core script of the project. Contains the main logic for browser automation (via remote debugging), traversing exams, and extracting questions, answers, and explanations.
- **`documentos_de_prueba/`**: A folder containing testing and development scripts (like `parse_dump.py` to `parse_dump6.py`, `debug.py`, and HTML dumps) used to iterate and refine BeautifulSoup extraction logic before integrating it into the main scraper.
- **`fix_json.py` & `verify_json.py`**: Utilities to clean up, structure, and validate the resulting `examen_completo.json` file to ensure the extracted data is correctly formatted.
- **`screenshot_stitch.py`, `check_images.py`, & `check_fixed.py`**: Helper scripts for managing, verifying, and potentially stitching downloaded diagrams and images linked to the exams.
- **`requirements.txt`**: Python dependencies required to run the project.

---

## Español

### Descripción General
Este repositorio contiene una robusta herramienta de automatización basada en Python que utiliza Selenium y BeautifulSoup para extraer (hacer scraping de) exámenes de práctica de Udemy. Específicamente, fue diseñada para extraer preguntas, opciones de respuesta, respuestas correctas, justificaciones detalladas y las imágenes incrustadas (diagramas) para el estudio fuera de línea y copias de seguridad.

### Características Principales
- **Evasión de Anti-Bots**: Utiliza un perfil de Chrome existente a través de depuración remota (`--remote-debugging-port`) para evadir Cloudflare y las protecciones estándar contra bots de Udemy.
- **Extracción de Exámenes Completos**: Itera a través de todos los tests de práctica de forma automática.
- **Descarga de Imágenes**: Identifica, descarga y mapea las imágenes incrustadas en las preguntas o respuestas a un directorio local `imagenes_examen`.
- **Salida Estructurada**: Compila todos los datos extraídos en un formato JSON estructurado (`examen_completo.json`) para su fácil análisis y uso en otras aplicaciones.

### Tecnologías Utilizadas
- Python
- Selenium WebDriver
- BeautifulSoup4
- Chrome Remote Debugging

### Estructura del Repositorio
- **`scraper.py`**: El script central del proyecto. Contiene toda la lógica principal de automatización (vía depuración remota), navegación por los exámenes y extracción de las preguntas, respuestas y justificaciones.
- **`documentos_de_prueba/`**: Carpeta que contiene scripts de prueba y desarrollo (como `parse_dump.py` a `parse_dump6.py`, `debug.py` y volcados HTML), utilizados para iterar y perfeccionar la lógica de extracción antes de integrarla en el scraper principal.
- **`fix_json.py` y `verify_json.py`**: Utilidades para limpiar, estructurar y validar el archivo resultante `examen_completo.json`, asegurando que los datos extraídos estén formateados correctamente.
- **`screenshot_stitch.py`, `check_images.py`, y `check_fixed.py`**: Scripts complementarios para manejar, verificar y procesar las imágenes y diagramas descargados vinculados a los exámenes.
- **`requirements.txt`**: Dependencias de Python necesarias para ejecutar el proyecto.
