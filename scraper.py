import os
import time
import json
import random
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup

# Configuración inicial
DEBUG_MODE = False # Si es True, solo extrae 2 preguntas por examen
DEBUG_QUESTIONS_LIMIT = 2

PORT = 9222 # Puerto de Chrome Debugging
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes_examen")

def init_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{PORT}")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def download_image(url, folder_path, image_name):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(folder_path, image_name)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return file_path
    except Exception as e:
        print(f"Error descargando imagen {url}: {e}")
    return None

def extract_images_from_element(element, folder_path, prefix):
    if not element:
        return []
        
    if hasattr(element, 'find_all'):
        images = element.find_all('img')
    else:
        images = element.find_elements(By.TAG_NAME, 'img')
        
    saved_images = []
    for idx, img in enumerate(images):
        src = img.get('src') if hasattr(img, 'get') else img.get_attribute('src')
        if src:
            ext = os.path.splitext(urlparse(src).path)[1]
            if not ext:
                ext = '.png'
            image_name = f"{prefix}_img_{idx}{ext}"
            local_path = download_image(src, folder_path, image_name)
            if local_path:
                saved_images.append(os.path.relpath(local_path, BASE_DIR))
    return saved_images

def scrape_udemy():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    driver = init_driver()
    wait = WebDriverWait(driver, 10)
    
    print("Conectado a Chrome exitosamente.")
    print("Asegúrate de estar en la página del curso de Udemy (Course content visible).")
    
    examen_completo = {}
    
    try:
        # Encontrar los examenes en el panel lateral (Course content)
        exam_links = driver.find_elements(By.CSS_SELECTOR, "div.item-link")
        
        if not exam_links:
            print("No se encontraron enlaces a exámenes. Asegúrate de tener el panel de contenido abierto.")
            return

        print(f"Se encontraron {len(exam_links)} elementos en el temario.")
        num_exams = len(exam_links)
        exam_counter = 1
        
        for exam_idx in range(num_exams):
            # Refrescar la lista para evitar StaleElementReferenceException
            exam_links = driver.find_elements(By.CSS_SELECTOR, "div.item-link")
            exam_link = exam_links[exam_idx]
            exam_title = exam_link.text.split('\n')[0].strip() or f"Examen_{exam_counter}"
            print(f"\n--- Iniciando {exam_title} ---")
            
            driver.execute_script("arguments[0].scrollIntoView();", exam_link)
            time.sleep(1)
            try:
                exam_link.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", exam_link)
            
            time.sleep(3) # Esperar a que cargue la vista
            
            # Verificar si ya estamos dentro del test
            preguntas_visibles = driver.find_elements(By.CSS_SELECTOR, "button[class*='question-navigation-item--title']")
            if len(preguntas_visibles) > 0:
                print("Ya estamos dentro del examen. Procediendo a extraer...")
            else:
                # Manejar las diferentes pantallas de inicio del examen
                try:
                    # 1. Verificar si hay un modal de "Your test is paused" con botón "Resume test"
                    time.sleep(1) # pausa breve para que el modal termine de animar si existe
                    resume_btn = driver.find_element(By.XPATH, "//button[contains(., 'Resume test')]")
                    print("Examen en pausa detectado. Resumiendo...")
                    resume_btn.click()
                except NoSuchElementException:
                    # 2. Si no hay modal, buscar la tarjeta de "Practice mode" (Examen nuevo)
                    try:
                        practice_mode_card = driver.find_element(By.XPATH, '//h4[text()="Practice mode"]/ancestor::div[@role="button"]')
                        print("Seleccionando Practice Mode para examen nuevo...")
                        practice_mode_card.click()
                        
                        # Dar tiempo a que cambie el DOM o aparezca "Begin test" si es necesario
                        time.sleep(1)
                        try:
                            begin_btn = driver.find_element(By.XPATH, "//button[contains(., 'Begin test') or contains(., 'Start test')]")
                            begin_btn.click()
                        except NoSuchElementException:
                            pass # A veces hacer click en la tarjeta lo inicia directamente
                            
                    except NoSuchElementException:
                        # 3. Opción de rescate
                        try:
                            alt_btn = driver.find_element(By.XPATH, "//button[contains(., 'Begin test') or contains(., 'Retake test') or contains(., 'Start test')]")
                            alt_btn.click()
                        except NoSuchElementException:
                            print("No se encontró forma de iniciar el test. Pasando al siguiente ítem...")
                            continue
            
            time.sleep(5) # Esperar a que cargue el examen
            
            exam_key = f"examen_{exam_counter}"
            exam_folder = os.path.join(IMAGES_DIR, exam_key)
            os.makedirs(exam_folder, exist_ok=True)
            
            preguntas_extraidas = []
            
            questions_nav = driver.find_elements(By.CSS_SELECTOR, "button[class*='question-navigation-item--title']")
            total_questions = len(questions_nav)
            print(f"Se encontraron {total_questions} preguntas en {exam_title}.")
            
            limit = DEBUG_QUESTIONS_LIMIT if DEBUG_MODE else total_questions
            
            for q_idx in range(min(total_questions, limit)):
                print(f"  Procesando pregunta {q_idx + 1}/{total_questions}...")
                
                questions_nav = driver.find_elements(By.CSS_SELECTOR, "button[class*='question-navigation-item--title']")
                q_btn = questions_nav[q_idx]
                driver.execute_script("arguments[0].scrollIntoView();", q_btn)
                time.sleep(1)
                
                # Cerrar modal de pausa si aparece
                try:
                    resume_btn = driver.find_element(By.XPATH, "//button[@data-purpose='unpause-test']")
                    if resume_btn.is_displayed():
                        print("    Cerrando modal de pausa...")
                        driver.execute_script("arguments[0].click();", resume_btn)
                        time.sleep(1)
                except NoSuchElementException:
                    pass

                try:
                    q_btn.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", q_btn)
                    
                time.sleep(2)
                
                q_data = {
                    "pregunta_numero": q_idx + 1,
                    "texto": "",
                    "imagenes_pregunta": [],
                    "opciones": [],
                    "explicacion": "",
                    "imagenes_explicacion": []
                }
                
                # Interactuar con la página para revelar las respuestas
                options = driver.find_elements(By.CSS_SELECTOR, "label[class*='mc-quiz-answer--answer'], div[class*='mc-quiz-answer--answer']")
                if options:
                    driver.execute_script("arguments[0].click();", options[0])
                        
                    try:
                        check_btn = driver.find_element(By.XPATH, "//button[contains(., 'Check answer')]")
                        driver.execute_script("arguments[0].click();", check_btn)
                        
                        # Esperar a que cargue la explicación
                        try:
                            wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(@class, 'ud-form-label') and contains(text(), 'Overall explanation')]")))
                        except TimeoutException:
                            pass
                    except NoSuchElementException:
                        pass
                
                # Extraer datos usando BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Extraer texto de la pregunta
                q_prompt = soup.find(id="question-prompt")
                if q_prompt:
                    q_data["texto"] = q_prompt.get_text(separator="\n", strip=True)
                    q_data["imagenes_pregunta"] = extract_images_from_element(q_prompt, exam_folder, f"q{q_idx+1}_pregunta")
                else:
                    print("    No se encontró el texto de la pregunta.")
                    continue
                
                # Extraer opciones
                options_soup = soup.select("ul[aria-labelledby='question-prompt'] > li")
                if not options_soup:
                    options_soup = soup.select("label[class*='mc-quiz-answer--answer']")
                if not options_soup:
                    # Estructura post-verificación de respuesta
                    qp = soup.find(id="question-prompt")
                    if qp:
                        for sibling in qp.find_next_siblings():
                            options_soup = sibling.select("div[data-purpose='answer']")
                            if options_soup:
                                break
                
                for o_idx, opt in enumerate(options_soup):
                    body_div = opt.select_one("div[class*='mc-quiz-answer--answer-body'], div[data-purpose='answer-body']")
                    opt_text = ""
                    if body_div:
                        text_div = body_div.select_one("div[class*='rt-scaffolding']") if "answer-body" in body_div.get("data-purpose", "") else None
                        opt_text = text_div.get_text(separator="\n", strip=True) if text_div else body_div.get_text(separator="\n", strip=True)
                    else:
                        opt_text = opt.get_text(separator="\n", strip=True)
                    
                    inner_html = str(opt)
                    is_correct = "Correct" in inner_html or "Correct selection" in inner_html or "ud-text-success" in inner_html
                    opt_imgs = extract_images_from_element(opt, exam_folder, f"q{q_idx+1}_opt{o_idx}")
                    
                    q_data["opciones"].append({
                        "texto": opt_text,
                        "es_correcta": is_correct,
                        "imagenes": opt_imgs
                    })
                
                # Extraer explicación
                expl_label = soup.find(lambda tag: tag.name == "label" and "Overall explanation" in tag.text)
                if expl_label:
                    expl_div = expl_label.find_next_sibling("div")
                    if expl_div:
                        q_data["explicacion"] = expl_div.get_text(separator="\n", strip=True)
                        q_data["imagenes_explicacion"] = extract_images_from_element(expl_div, exam_folder, f"q{q_idx+1}_expl")
                else:
                    print("    No se encontró justificación/explicación.")
                
                preguntas_extraidas.append(q_data)
                
                if q_idx < limit - 1:
                    sleep_time = random.randint(30, 45)
                    print(f"    Esperando {sleep_time}s antes de la siguiente pregunta...")
                    time.sleep(sleep_time)
            
            examen_completo[exam_key] = {
                "titulo": exam_title,
                "preguntas": preguntas_extraidas
            }
            exam_counter += 1
            
            try:
                close_btn = driver.find_element(By.XPATH, "//button[@data-purpose='close-quiz-test-view'] | //a[contains(@class, 'header--close')] | //a[@aria-label='Back to course']")
                close_btn.click()
                time.sleep(3)
            except NoSuchElementException:
                driver.back()
                time.sleep(3)
                
            with open(os.path.join(BASE_DIR, "examen_completo.json"), 'w', encoding='utf-8') as f:
                json.dump(examen_completo, f, ensure_ascii=False, indent=4)
                
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        with open(os.path.join(BASE_DIR, "examen_completo.json"), 'w', encoding='utf-8') as f:
            json.dump(examen_completo, f, ensure_ascii=False, indent=4)
        print("Scraping finalizado. Datos guardados en examen_completo.json")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    scrape_udemy()
