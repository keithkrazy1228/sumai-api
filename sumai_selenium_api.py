from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Sumai Step API is live!"

@app.route('/api/get_customer_info', methods=['POST'])
def get_customer_info():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        url = data.get("url")
        if not url:
            return jsonify({"error": "Missing 'url' in request"}), 400

        property_id = url.split("/")[-1]

        # ChromeDriver setup for Render
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.binary_location = "/usr/bin/google-chrome"
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".assessment-request_value"))
        )

        values = driver.find_elements(By.CSS_SELECTOR, ".assessment-request_value")
        date_received = values[0].text
        property_address = values[3].text
        year_built = values[7].text

        applicant_info = driver.find_elements(By.CSS_SELECTOR, '.box.applicant td:nth-child(2)')
        name = applicant_info[0].text
        age = applicant_info[2].text
        phone = applicant_info[3].text
        email = applicant_info[4].text

        result = {
            "property_id": property_id,
            "date_received": date_received,
            "property_address": property_address,
            "year_built": year_built,
            "applicant_name": name,
            "applicant_age": age,
            "applicant_phone": phone,
            "applicant_email": email
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
