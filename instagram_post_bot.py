import os
import requests
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Load environment variables
load_dotenv()
print("Environment variables loaded.")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
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
        print(f"Requested image from Unsplash. Status code: {response.status_code}")
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        print(f"Response from Unsplash: {data}")
        if not data:
            raise Exception("No images found or invalid response from Unsplash API")
        image_url = data[0]['urls']['regular']
        logger.info(f'Fetched image URL: {image_url}')
        print(f"Fetched image URL: {image_url}")
        return image_url
    except requests.exceptions.RequestException as e:
        logger.error(f'Failed to fetch image from Unsplash API: {e}')
        print(f"Failed to fetch image from Unsplash API: {e}")
        raise
    except Exception as e:
        logger.error(f'Error in get_random_image function: {e}')
        print(f"Error in get_random_image function: {e}")
        raise

def post_to_instagram(image_url, caption):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        service = ChromeService(executable_path=ChromeDriverManager().install())
        print("ChromeDriver installed.")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized.")
        driver.get("https://www.instagram.com/accounts/login/")
        logger.info("Opened Instagram login page")
        print("Opened Instagram login page.")

        wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds for elements to appear

        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        username_field.send_keys(os.getenv('INSTAGRAM_USERNAME'))
        print(f"Entered username: {os.getenv('INSTAGRAM_USERNAME')}")

        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        password_field.send_keys(os.getenv('INSTAGRAM_PASSWORD'))
        print(f"Entered password: {os.getenv('INSTAGRAM_PASSWORD')}")

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        logger.info("Logged into Instagram")
        print("Logged into Instagram.")

        # Wait for the home page to load by waiting for the profile icon
        profile_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@aria-label='Profile']")))

        driver.get("https://www.instagram.com/create/style/")
        logger.info("Opened Instagram post page")
        print("Opened Instagram post page.")

        # Capture a screenshot to verify page state
        driver.save_screenshot('post_page.png')
        logger.info("Captured screenshot of the post page")

        # Wait for the file input to be present
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        upload_input.send_keys(image_url)
        logger.info(f"Uploaded image: {image_url}")
        print(f"Uploaded image: {image_url}")

        # Capture a screenshot to verify the image upload
        driver.save_screenshot('image_uploaded.png')
        logger.info("Captured screenshot after image upload")

        caption_field = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Write a caption…']")))
        caption_field.send_keys(caption)
        print(f"Entered caption: {caption}")

        share_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Share')]")))
        share_button.click()
        logger.info("Posted to Instagram")
        print("Posted to Instagram.")

        driver.quit()
        print("WebDriver closed.")
    except Exception as e:
        logger.error(f'Error in post_to_instagram function: {e}')
        print(f'Error in post_to_instagram function: {e}')
        if 'driver' in locals():
            driver.quit()
            print("WebDriver closed due to error.")
        raise

def main():
    try:
        image_url = get_random_image()
        caption = "Time and Hard Work: The Key to Success! 💪 #Motivation #HardWork #Success #Dedication #Inspiration #StayStrong"
        post_to_instagram(image_url, caption)
        logger.info(f'Posted image at {datetime.now()}')
        print(f'Posted image at {datetime.now()}')
    except Exception as e:
        logger.error(f'Error in main function: {e}')
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()
