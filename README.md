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
