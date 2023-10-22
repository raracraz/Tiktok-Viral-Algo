from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import configparser
import sys

# Reading from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

username = config['account']['username']
password = config['account']['password']

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--detached --incognito --window-size=1920x1080")
chrome_options.add_argument("--user-data-dir=/temp_profile")

# Set up Selenium WebDriver (e.g., using Chrome)
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

# Navigate to TikTok login page
driver.get("https://www.tiktok.com/login/phone-or-email/email")

# Delete all cookies after navigating to the page
driver.delete_all_cookies()

# Enter your username and password
# username_field = driver.find_element(By.NAME, "username")  # Replace 'username' with the actual field name
# password_field = driver.find_element(By.NAME, "password")  # Replace 'password' with the actual field name

time.sleep(2)

try:
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)  # Press Enter to log in
except:
    print("Login failed!")
    sys.exit(1)

# Wait for login to complete, Check if login was successful by checking the URL, 
# if after 10 seconds the url is not https://www.tiktok.com/foryou, then exit the program
try:
    WebDriverWait(driver, 60).until(EC.url_to_be("https://www.tiktok.com/foryou"))
    print("Login successful!")
    driver.save_screenshot("screenshots/screenshot.png")
except:
    print("Login failed!")
    driver.save_screenshot("screenshots/screenshot.png")
    sys.exit(1)

# At the end of your script, delete the custom user data directory
driver.quit()  # Ensure the browser is closed before deleting the directory
shutil.rmtree("/temp_profile")