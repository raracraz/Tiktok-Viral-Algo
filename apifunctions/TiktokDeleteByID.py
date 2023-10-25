import time
import configparser
import sys
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Reading from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

sessionid = config['cookie']['sessionid']
username = config['cookie']['username'] 

video_id = config['tiktok']['videoid']

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--detached")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--user-data-dir=/temp_profile")  # Set the correct path for the user data directory
# chrome_options.add_argument(f"--proxy-server=http://localhost:8080")
# chrome_options.add_argument("--ignore-certificate-errors")

# Set up Selenium WebDriver (e.g., using Chrome)
driver = webdriver.Chrome(options=chrome_options)

# Navigate to TikTok login page
driver.get("https://www.tiktok.com")

# set the sessionid cookie
driver.add_cookie({'name': 'sessionid', 'value': sessionid})

# Refresh the page
driver.refresh()

# Add a flag to track whether the video deletion was successful
video_deleted_successfully = False

def delete_video(video_id):
    global video_deleted_successfully
    
    # Now you can get the cookies
    cookies = driver.get_cookies()

    # Optionally, you could convert this list of dictionaries to a single dictionary for easier use:
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    
    # Convert the cookies_dict to a cookies string
    cookies_string = '; '.join([f'{name}={value}' for name, value in cookies_dict.items()])
    
    # Headers from your successful Postman delete request
    # [{"key":"sec-ch-ua","value":"\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Opera GX\";v=\"102\""},{"key":"content-type","value":"application/x-www-form-urlencoded"},{"key":"x-secsdk-csrf-token","value":"0001000000013e6e45a29ebfa8debb51fc4709401de5bd7dc010a974789c5b5c6d673897e0bb179141431abcd9e5"},{"key":"tt-csrf-token","value":"f3yJULJf-c9ox8doluOV0ynrd9lBpG5qP3s0"},{"key":"User-Agent","value":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0"},{"key":"sec-ch-ua-mobile","value":"?0"},{"key":"sec-ch-ua-platform","value":"\"Windows\""},{"key":"Accept","value":"*/*"},{"key":"host","value":"www.tiktok.com"}]
    
    headers = {
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Opera GX\";v=\"102\"",
        "content-type": "application/x-www-form-urlencoded",
        "x-secsdk-csrf-token": "0001000000013e6e45a29ebfa8debb51fc4709401de5bd7dc010a974789c5b5c6d673897e0bb179141431abcd9e5",
        "tt-csrf-token": "f3yJULJf-c9ox8doluOV0ynrd9lBpG5qP3s0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Accept": "*/*",
        "host": "www.tiktok.com",
        "Origin": "https://www.tiktok.com",
        "Content-Length": "0",
        "Cookie": cookies_string  # Assuming cookies_string is defined and formatted correctly
    }
    
    js_script = f"""
    return new Promise((resolve, reject) => {{
        const url = "https://www.tiktok.com/api/aweme/delete/?aweme_id={video_id}&target={video_id}";
        const options = {{
            method: 'POST',
            headers: {headers},
            credentials: 'include'
        }};
        fetch(url, options)
            .then(response => {{
                if (response.ok) {{
                    resolve("Video deleted successfully!");
                }} else {{
                    response.text().then(text => {{
                        reject("Failed to delete video: " + response.statusText + ", Response body: " + (text || "No response body"));
                    }}).catch(error => reject("Failed to read response body: " + error.message));
                }}
            }})
            .catch(error => reject("Fetch error: " + error.message));
    }});
    """

    # Execute the JavaScript code
    try:
        result = driver.execute_script(js_script)
        print(result)
        video_deleted_successfully = True
    except Exception as e:
        print(f"An error occurred: {e}")
        video_deleted_successfully = False

# Wait for login to complete, Check if login was successful by checking the URL, 
# if after 10 seconds the url is not https://www.tiktok.com/foryou, then exit the program
try:
    WebDriverWait(driver, 10).until(EC.url_to_be("https://www.tiktok.com/explore"))
    print("Login successful!")
    
    # go to the profile page
    profile_url = f"https://www.tiktok.com/@{username}"
    driver.get(profile_url)
    print(f"Navigated to profile page of user: {username}")
    
    try:
        # if delete video function fails, print error and exit
        delete_video(int(video_id))
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
        
except:
    print("Login failed!")
    driver.save_screenshot("screenshot.png")
    sys.exit(1)

# At the end of your script, delete the custom user data directory
if not video_deleted_successfully:  # Only quit the driver and delete the directory if the video wasn't deleted successfully
    driver.quit()  # Ensure the browser is closed before deleting the directory
    shutil.rmtree("/temp_profile")