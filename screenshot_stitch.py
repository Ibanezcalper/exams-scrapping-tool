from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.get("https://stitch.withgoogle.com/projects/9057933980437615668")
time.sleep(10) # wait for SPA to load
driver.save_screenshot("stitch_screenshot.png")
driver.quit()
print("Screenshot saved to stitch_screenshot.png")
