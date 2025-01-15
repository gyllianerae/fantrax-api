import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def login_and_save_cookie():
    print("Starting ChromeDriver...")  # Debug message
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--window-size=1920,1600")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get("https://www.fantrax.com/login")
        print("Please log in to Fantrax manually...")
        time.sleep(30)  # Time to manually log in
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

# Add this to call the function
if __name__ == "__main__":
    login_and_save_cookie()
