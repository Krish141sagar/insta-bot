import os
import requests
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(filename='bot.log', level=logging.INFO)
logger = logging.getLogger()

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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.instagram.com/accounts/login/")
        logger.info("Opened Instagram login page")

        driver.find_element(By.NAME, 'username').send_keys(os.getenv('INSTAGRAM_USERNAME'))
        driver.find_element(By.NAME, 'password').send_keys(os.getenv('INSTAGRAM_PASSWORD'))
        driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]").click()
        logger.info("Logged into Instagram")

        driver.get("https://www.instagram.com/create/style/")
        logger.info("Opened Instagram post page")

        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(image_url)
        logger.info(f"Uploaded image: {image_url}")

        driver.find_element(By.XPATH, "//textarea[@aria-label='Write a caption…']").send_keys(caption)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Share')]").click()
        logger.info("Posted to Instagram")

        driver.quit()
    except Exception as e:
        logger.error(f'Error in post_to_instagram function: {e}')
        if 'driver' in locals():
            driver.quit()
        raise

def main():
    try:
        image_url = get_random_image()
        caption = "Time and Hard Work: The Key to Success! 💪 #Motivation #HardWork #Success #Dedication #Inspiration #StayStrong"
        post_to_instagram(image_url, caption)
        logger.info(f'Posted image at {datetime.now()}')
    except Exception as e:
        logger.error(f'Error in main function: {e}')

if __name__ == "__main__":
    main()
