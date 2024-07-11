import os
import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def get_random_image():
    url = "https://api.unsplash.com/photos/random"
    params = {
        'client_id': os.getenv('UNSPLASH_ACCESS_KEY'),
        'query': 'motivational',
        'count': 1  # Request one image
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        if not data:
            raise Exception("No images found or invalid response from Unsplash API")
        image_url = data[0]['urls']['regular']
        logger.info(f'Fetched image URL: {image_url}')
        return image_url
    except requests.exceptions.RequestException as e:
        logger.error(f'Failed to fetch image from Unsplash API: {e}')
        raise
    except Exception as e:
        logger.error(f'Error in get_random_image function: {e}')
        raise


def post_to_instagram(image_url, caption):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get('https://www.instagram.com/accounts/login/')
        wait = WebDriverWait(driver, 30)
        
        logger.info("Waiting for username field...")
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys(os.getenv('INSTAGRAM_USERNAME'))

        logger.info("Waiting for password field...")
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(os.getenv('INSTAGRAM_PASSWORD'))

        logger.info("Submitting login form...")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
        login_button.click()

        logger.info("Logged into Instagram.")

        time.sleep(5)  # Adjust sleep time as needed to wait for login to complete

        # Check for not now buttons and dismiss them
        try:
            not_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]')))
            not_now_button.click()
            logger.info("Clicked 'Not Now' on save login info prompt.")
        except NoSuchElementException:
            pass

        try:
            not_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]')))
            not_now_button.click()
            logger.info("Clicked 'Not Now' on turn on notifications prompt.")
        except NoSuchElementException:
            pass

        # Simulate image upload
        driver.get('https://www.instagram.com/')
        new_post_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="New Post"]')))
        new_post_button.click()

        logger.info("Clicked on new post button.")

        upload_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
        upload_input.send_keys(os.path.abspath("local_path_to_your_image.jpg"))

        logger.info("Uploaded image.")

        # Add a caption
        caption_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Write a caption…"]')))
        caption_field.send_keys(caption)

        logger.info("Added caption.")

        share_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Share")]')))
        share_button.click()

        logger.info(f"Posted image at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        logger.error(f"Error in post_to_instagram function: {e}")
        driver.save_screenshot('debug_screenshot.png')
        logger.info("Saved screenshot for debugging.")
    finally:
        driver.quit()
        logger.info("WebDriver closed.")

def main():
    logger.info("Starting Instagram bot...")
    
    logger.info(f"INSTAGRAM_USERNAME: {os.getenv('INSTAGRAM_USERNAME')}")
    logger.info(f"INSTAGRAM_PASSWORD: {os.getenv('INSTAGRAM_PASSWORD')}")
    logger.info(f"UNSPLASH_ACCESS_KEY: {os.getenv('UNSPLASH_ACCESS_KEY')}")

    image_url = get_random_image()
    caption = "Stay motivated! #motivation #inspiration #hardwork #success #goals"
    post_to_instagram(image_url, caption)

if __name__ == "__main__":
    main()
