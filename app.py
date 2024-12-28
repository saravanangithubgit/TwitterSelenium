import os
import logging
from flask import Flask, json, render_template, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
import aiohttp
import requests  # Import the requests library
from urllib.parse import quote as url_quote

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch DATABASE_URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Function to fetch public IP
async def fetch_public_ip():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.ipify.org') as response:
            return await response.text()

# Function to fetch all records from the database
async def fetch_all_records():
    async with aiohttp.ClientSession() as session:
        async with session.get(DATABASE_URL) as response:
            if response.status != 200:
                return {"error": f"Failed to fetch data: {response.status}"}
            return await response.json()

# Function to send data to the database
def send_to_database(data):
    response = requests.post(DATABASE_URL, json=data)
    if response.status_code == 201:
        print("Data successfully sent to the database")
    else:
        print(f"Failed to send data to the database: {response.status_code} {response.text}")

# Function to log in to Twitter and get trends
async def twitter_login_and_get_attributes():
    proxy_pac_url = "http://localhost:8080/proxy.pac"  # Path to your PAC file served by local server
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"--proxy-pac-url={proxy_pac_url}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Starting browser and navigating to Twitter login page")
        driver.get("https://twitter.com/login")
        print("Navigated to Twitter login page")

        # Enter username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@name="text"]'))
        )
        username_field.send_keys("saravan19212894")
        print("Username entered successfully")

        # Click next button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]'))
        )
        next_button.click()
        print("Next button clicked successfully")

        # Check if email field is required
        try:
            email_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'))
            )
            email_field.send_keys("saravananannewday@gmail.com")
            print("Email entered successfully")

            next_button_again = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button'))
            )
            next_button_again.click()
            print("Next button clicked again")
        except Exception as e:
            print(f"Email field not required: {e}")

        # Enter password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@name="password"]'))
        )
        password_field.send_keys("clashofclans")
        print("Password entered successfully")

        # Click login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button'))
        )
        login_button.click()
        print("Login button clicked successfully")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Timeline: Trending now"]'))
        )
        print("Logged in successfully")

        # Click on the "Show more" link
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/explore/tabs/for-you"]//span[contains(text(), "Show more")]'))
        )
        show_more_button.click()
        print("Clicked 'Show more' button")

        # Collect text content for trends
        span_xpath = '//span[@dir="ltr" and contains(@class, "css-1jxf684")]'
        trend_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, span_xpath))
        )
        top_5_trends = [trend.text for trend in trend_elements[:5]]
        print("Collected top 5 trends")

        # Fetch public IP address asynchronously
        public_ip = await fetch_public_ip()

        data = {
            "currentTime": datetime.now().strftime("%Y-%m-%d %I:%S %p"),
            "publicIp": public_ip,
            "trends": top_5_trends
        }
        driver.implicitly_wait(5)
        driver.quit()
        print("Browser closed successfully")
        
        # Send data to the database
        send_to_database(data)
        
        return data

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['GET'])
async def run_script():
    selenium_data = await twitter_login_and_get_attributes()  # Run your Selenium script and get one data set
    if "error" in selenium_data:
        return jsonify({"error": selenium_data["error"]}), 500
    
    records = await fetch_all_records()  # Fetch all records from your API endpoint
    if "error" in records:
        return jsonify({"error": records["error"]}), 500
    
    # Combine selenium_data and records into one response
    combined_data = {
        "selenium_data": selenium_data,
        "db_data": records
    }
    
    return app.response_class(
        response=json.dumps(combined_data, ensure_ascii=False),  # Disable ASCII encoding
        status=200,
        mimetype="application/json"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
