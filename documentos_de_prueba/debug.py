import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def debug_dom():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    
    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("DOM dumped to page_dump.html")

if __name__ == "__main__":
    debug_dom()
