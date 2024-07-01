from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import random
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Instagram credentials and Unsplash access key
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')
unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY')

# Define hashtags
hashtags = ["#motivation", "#inspiration", "#success", "#life", "#happy", "#mindset", "#believe", "#growth", "#positivity", "#goal"]

# Get a random motivational image from Unsplash
def get_random_image():
    response = requests.get(f'https://api.unsplash.com/photos/random?query=motivational&client_id={unsplash_access_key}')
    data = response.json()
    image_url = data[0]['urls']['regular']
    return image_url

# Download the image
def download_image(image_url):
    response = requests.get(image_url)
    with open('motivation_image.jpg', 'wb') as file:
        file.write(response.content)

# Instagram login and post image
def post_to_instagram():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    service = Service('/path/to/chromedriver')  # Replace with the path to your chromedriver
    driver = webdriver.Chrome(service=service, options=options)  # Updated initialization

    driver.get('https://www.instagram.com/accounts/login/')

    time.sleep(5)
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    time.sleep(5)
    driver.get('https://www.instagram.com/create/style/')

    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(os.path.abspath('motivation_image.jpg'))

    time.sleep(5)
    caption = "Motivational Quote!\n" + " ".join(random.sample(hashtags, 5))
    driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Write a caption…"]').send_keys(caption)

    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'button[type="button"]').click()

    time.sleep(5)
    driver.quit()

# Main function
def main():
    image_url = get_random_image()
    download_image(image_url)
    post_to_instagram()

if __name__ == "__main__":
    main()
