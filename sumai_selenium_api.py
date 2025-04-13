from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Sumai Step API is live!"

@app.route('/api/get_customer_info', methods=['POST'])
def get_customer_info():
    try:
        data = request.get_json(force=True)
        url = data.get("url")

        if not url:
            return jsonify({"error": "Missing 'url' in request"}), 400

        # ✅ Selenium設定（Render用）
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/usr/bin/chromium"
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        # ✅ ログイン処理（住まいステップ）
        driver.get("https://sumai-step.com/partner/login")
        time.sleep(2)
        driver.find_element(By.NAME, "partner[email]").send_keys("kenou-akimoto@a2gjpn.co.jp")
        driver.find_element(By.NAME, "partner[password]").send_keys("kenouestate2024")
        driver.find_element(By.NAME, "commit").click()
        time.sleep(2)

        # ✅ 顧客情報ページに遷移
        driver.get(url)
        time.sleep(2)

        print("📸 現在のURL:", driver.current_url)
        print("🧱 HTMLの冒頭:", driver.page_source[:1000])

        # ✅ 顧客情報の抽出（XPath仮設定）※要修正する可能性あり
        name = driver.find_element(By.XPATH, '//*[@id="conversion_detail"]/div[1]/table/tbody/tr[1]/td').text
        address = driver.find_element(By.XPATH, '//*[@id="conversion_detail"]/div[1]/table/tbody/tr[2]/td').text
        tel = driver.find_element(By.XPATH, '//*[@id="conversion_detail"]/div[1]/table/tbody/tr[3]/td').text

        return jsonify({
            "name": name,
            "address": address,
            "tel": tel
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
