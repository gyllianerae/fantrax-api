import pickle
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def login_and_save_cookie():
    print("Starting ChromeDriver...")  # Debug message
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1600")

    # Possible Chrome binary paths
    chrome_binary_paths = ["/usr/bin/google-chrome", "/opt/google/chrome/google-chrome", "/usr/local/bin/google-chrome"]

    for path in chrome_binary_paths:
        if os.path.exists(path):
            options.binary_location = path
            print(f"Using Chrome binary at: {path}")
            break
    else:
        raise Exception("Google Chrome binary not found!")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get("https://www.fantrax.com/login")
        print("Please log in to Fantrax manually...")
        time.sleep(30)  # Time for manual login
        cookies = driver.get_cookies()
        if cookies:
            pickle.dump(cookies, open("fantraxloggedin.cookie", "wb"))
            print("Cookie saved as fantraxloggedin.cookie")
            with open("login_status.txt", "w") as f:
                f.write("success")  # Write success status
        else:
            print("No cookies found. Ensure you logged in manually.")
            with open("login_status.txt", "w") as f:
                f.write("failed")  # Write failure status

if __name__ == "__main__":
    login_and_save_cookie()
