import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def post_to_instagram(image_url, caption):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("WebDriver initialized.")

        driver.get("https://www.instagram.com/accounts/login/")
        logger.info("Opened Instagram login page")

        wait = WebDriverWait(driver, 30)  # Increased wait time to 30 seconds

        try:
            username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
            username_field.send_keys(os.getenv('INSTAGRAM_USERNAME'))
            logger.info(f"Entered username: {os.getenv('INSTAGRAM_USERNAME')}")
        except TimeoutException:
            logger.error("Timeout while waiting for the username field")
            return

        try:
            password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
            password_field.send_keys(os.getenv('INSTAGRAM_PASSWORD'))
            logger.info("Entered password.")
        except TimeoutException:
            logger.error("Timeout while waiting for the password field")
            return

        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            login_button.click()
            logger.info("Logged into Instagram.")
        except TimeoutException:
            logger.error("Timeout while waiting for the login button")
            return

        # Wait for the page to load after login
        time.sleep(10)  # Static wait for the page to load; adjust as needed
        driver.get("https://www.instagram.com/create/style/")
        logger.info("Opened Instagram post page.")

        try:
            upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            upload_input.send_keys(image_url)
            logger.info(f"Uploaded image: {image_url}")
        except TimeoutException:
            logger.error("Timeout while waiting for the file input")
            driver.save_screenshot('debug_screenshot.png')
            logger.info("Saved screenshot for debugging")
            return

        try:
            caption_field = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Write a caption…']")))
            caption_field.send_keys(caption)
            logger.info(f"Entered caption: {caption}")
        except TimeoutException:
            logger.error("Timeout while waiting for the caption field")
            return

        try:
            share_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Share')]")))
            share_button.click()
            logger.info("Posted to Instagram.")
        except TimeoutException:
            logger.error("Timeout while waiting for the share button")
            return

        driver.quit()
        logger.info("WebDriver closed.")
    except NoSuchElementException as e:
        logger.error(f'Element not found: {e}')
        if 'driver' in locals():
            driver.quit()
    except TimeoutException as e:
        logger.error(f'Timeout waiting for element: {e}')
        if 'driver' in locals():
            driver.quit()
    except Exception as e:
        logger.error(f'Error in post_to_instagram function: {e}')
        if 'driver' in locals():
            driver.quit()
        raise

def main():
    image_url = "/path/to/your/image.jpg"  # Replace with your local image path
    caption = "This is a test caption."  # Replace with your desired caption
    post_to_instagram(image_url, caption)
    logger.info(f"Posted image at {datetime.now()}")

if __name__ == "__main__":
    main()
