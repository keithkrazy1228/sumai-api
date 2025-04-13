from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Sumai Step API is live!"

@app.route('/api/get_customer_info', methods=['POST'])
def get_customer_info():
    data = request.get_json()
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "URLが見つかりません"}), 400

    # 管理番号をURLから抽出
    property_id = url.split("/")[-1]

    # ChromeDriver設定
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)  # ページ読み込み待機

        # --- 物件情報 ---
        values = driver.find_elements(By.CSS_SELECTOR, ".assessment-request_value")
        date_received = values[0].text
        property_address = values[3].text
        year_built = values[7].text

        # --- 申込者情報 ---
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
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
