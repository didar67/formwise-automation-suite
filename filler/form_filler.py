from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from core.logger import logger
from datetime import datetime
import os
from core.utils import retry
from core.webdriver_manager import get_chrome_driver

BY_MAP = {
    'id': By.ID, 'name': By.NAME, 'xpath': By.XPATH,
    'css_selector': By.CSS_SELECTOR, 'class_name': By.CLASS_NAME,
    'tag_name': By.TAG_NAME, 'link_text': By.LINK_TEXT, 'partial_link_text': By.PARTIAL_LINK_TEXT,
}

def take_screenshot(driver, name_prefix="error"):
    time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{name_prefix}_{time}.png"
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(filename)
    logger.info(f"Screenshot saved: {filename}")

@retry(retries=3, delay=2)
def fill_form(config, dry_run=False, headless=True):
    driver = get_chrome_driver(headless)
    try:
        logger.info(f"Navigating to {config.url}")
        driver.get(config.url)
        WebDriverWait(driver, 20).until(lambda d: d.execute_script("return document.readyState")== "complete")

        for field in config.fields:
            try:
                by = BY_MAP[field.locator.by]
                locator_val = field.locator.value
                logger.info(f"Filling {field.type} by {field.locator.by}= '{locator_val}' with value '{field.value}'")
                element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((by, locator_val)))

                if field.type == "text":
                    element.clear()
                    element.send_keys(field.value)
                elif field.type == "checkbox":
                    if field.value.lower() == "true" and not element.is_selected():
                        element.click()
                elif field.type == "radio":
                    element.click()
                elif field.type == "dropdown":
                    Select(element).select_by_visible_text(field.value)

            except TimeoutException:
                logger.warning(f"Field ({field.locator.by}='{field.locator.value}') not found.")
                continue
            
        # CAPTCHA Handling (Manual or placeholder for 3rd-party or AI-based solvers)
        try:
            captcha = driver.find_element(By.CLASS_NAME, "captcha")
            logger.warning("🛑 CAPTCHA detected. Awaiting manual intervention or integrate a solver.")
            input("Press Enter to continue and Solve CAPTCHA.")
        except NoSuchElementException:
            logger.info('No CAPTCHA found.')

        if not dry_run:
            submit_by = BY_MAP[config.submit_button.locator.by]
            submit_val = config.submit_button.locator.value
            logger.info(f"Clicking submit button by {config.submit_button.locatorby}='{submit_val}'")
            submit_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((submit_by, submit_val)))
            submit_btn.click()
            logger.info("Form submitted successfully")

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[conatins(text(), 'Thank you')]")))
                logger.info("Submission verified: 'Thank you' message found.")
            except TimeoutException:
                logger.warning("No post-submission confirmation message found.")

        else:
            logger.info("Dry run enable.")

    except WebDriverException as e:
        logger.error(f"Webdriver error: {e}")
        take_screenshot(driver, "webdriver_error")
        raise
    
    finally:
        driver.quit()