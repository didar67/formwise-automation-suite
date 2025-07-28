"""
WebDriver manager for automatic driver installation and setup.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--diable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager(). install()), options=options)