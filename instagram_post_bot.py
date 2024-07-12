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

        wait = WebDriverWait(driver, 15)  # Wait up to 15 seconds for elements to appear

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
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[@aria-label='Profile']")))

        driver.get("https://www.instagram.com/create/style/")
        logger.info("Opened Instagram post page")
        print("Opened Instagram post page.")

        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        upload_input.send_keys(image_url)
        logger.info(f"Uploaded image: {image_url}")
        print(f"Uploaded image: {image_url}")

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
