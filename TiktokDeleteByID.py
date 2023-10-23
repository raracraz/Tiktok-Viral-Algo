import time
import configparser
import sys
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Reading from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

sessionid = config['cookie']['sessionid']

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--detached")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--user-data-dir=/temp_profile")  # Set the correct path for the user data directory

# Set up Selenium WebDriver (e.g., using Chrome)
driver = webdriver.Chrome(options=chrome_options)

# Navigate to TikTok login page
driver.get("https://www.tiktok.com")

# Add the session ID to the cookies
driver.add_cookie({'name': 'sessionid', 'value': sessionid})

# Refresh the page
driver.refresh()

# Wait for login to complete, Check if login was successful by checking the URL, 
# if after 10 seconds the url is not https://www.tiktok.com/foryou, then exit the program
try:
    WebDriverWait(driver, 10).until(EC.url_to_be("https://www.tiktok.com/explore"))
    print("Login successful!")
    
    # go to the profile page
    
    
    
except:
    print("Login failed!")
    driver.save_screenshot("screenshot.png")
    sys.exit(1)

# At the end of your script, delete the custom user data directory
driver.quit()  # Ensure the browser is closed before deleting the directory
shutil.rmtree("/temp_profile")