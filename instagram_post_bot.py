import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)

def get_random_image():
    logging.info("Fetching random image from Unsplash API")
    import requests

    url = f"https://api.unsplash.com/photos/random?client_id={os.getenv('UNSPLASH_ACCESS_KEY')}&query=motivational"
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f"Unsplash API request failed with status {response.status_code}")
        raise Exception("Failed to fetch image from Unsplash API")

    data = response.json()
    if not data or 'urls' not in data[0]:
        logging.error("No images found or invalid response from Unsplash API")
        raise Exception("No images found or invalid response from Unsplash API")

    image_url = data[0]['urls']['regular']
    logging.info(f"Fetched image URL: {image_url}")
    return image_url

def post_to_instagram(image_url, caption):
    logging.info("Starting Instagram posting process")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run headless for GitHub Actions
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 30)

        driver.get("https://www.instagram.com/accounts/login/")

        # Login
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(os.getenv('INSTAGRAM_USERNAME'))
        password_field.send_keys(os.getenv('INSTAGRAM_PASSWORD'))
        password_field.send_keys(u'\ue007')  # Press Enter key
        logging.info("Logged into Instagram")

        # Wait for login to complete
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav")))

        # Post image
        driver.get("https://www.instagram.com/create/style/")
        upload_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        upload_input.send_keys(image_url)  # Upload the image URL

        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Next')]")))
        next_button.click()

        caption_field = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Write a caption…']")))
        caption_field.send_keys(caption)

        share_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Share')]")))
        share_button.click()
        logging.info("Image posted to Instagram")

        driver.save_screenshot('debug_screenshot.png')
    except Exception as e:
        logging.error(f"Error in post_to_instagram function: {e}")
        driver.save_screenshot('debug_screenshot.png')
        raise
    finally:
        driver.quit()
        logging.info("WebDriver closed.")

def main():
    try:
        image_url = get_random_image()
        caption = "Stay motivated! #motivation #inspiration #hardwork #success"
        post_to_instagram(image_url, caption)
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
