import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

# Get credentials from environment variables
username = os.getenv('i_can_do_to_change')
password = os.getenv('Krish$141')
unsplash_access_key = os.getenv('AtiNcai83k5PAWXd02hOWYPhbghlWANA6GFsUhZGKBs')

# List of motivational hashtags
hashtags = [
    "#Motivation", "#Inspiration", "#StayPositive", "#Believe", "#Success", 
    "#PositiveVibes", "#DreamBig", "#KeepGoing", "#StayStrong", "#YouCanDoIt",
    "#NeverGiveUp", "#WorkHard", "#GoalSetting", "#SelfImprovement", "#Mindset",
    "#MotivationalQuotes", "#DailyInspiration", "#LifeGoals", "#PushYourLimits"
]

# Function to download a random motivational image from Unsplash
def download_random_image():
    url = f'https://api.unsplash.com/photos/random?query=motivational&client_id={unsplash_access_key}'
    response = requests.get(url).json()
    image_url = response['urls']['regular']
    image_data = requests.get(image_url).content

    with open('motivational_image.jpg', 'wb') as handler:
        handler.write(image_data)

    return 'motivational_image.jpg'

# Initialize the WebDriver
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Make sure to provide the correct path

try:
    # Random delay between -17 and +17 minutes (1020 seconds)
    random_delay = random.randint(-1020, 1020)
    time.sleep(random_delay)

    # Download a random motivational image
    image_path = download_random_image()

    # Open Instagram and log in
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)  # Allow time for the page to load

    # Find and fill the username and password fields
    username_field = driver.find_element_by_name("username")
    password_field = driver.find_element_by_name("password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Allow time for the login process

    # Navigate to the post upload page
    driver.get("https://www.instagram.com/create/style/")
    time.sleep(5)  # Allow time for the page to load

    # Upload the image
    upload_input = driver.find_element_by_css_selector("input[type='file']")
    upload_input.send_keys(os.path.abspath(image_path))
    time.sleep(5)  # Allow time for the image to upload

    # Enter the caption
    caption = "Here's your daily dose of motivation! " + " ".join(hashtags)
    caption_field = driver.find_element_by_css_selector("textarea[aria-label='Write a caption…']")
    caption_field.send_keys(caption)

    # Share the post
    share_button = driver.find_element_by_xpath("//button[contains(text(),'Share')]")
    share_button.click()

    time.sleep(5)  # Allow time for the post to be shared

finally:
    # Close the WebDriver
    driver.quit()
    # Remove the downloaded image
    os.remove(image_path)
