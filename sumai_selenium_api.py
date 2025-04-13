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

        print("🟡 Selenium起動OK")

        # ✅ ログインページへアクセス
        driver.get("https://sumai-step.com/partner/login")
        print("➡️ ログインページ到達:", driver.current_url)
        time.sleep(2)

        # ✅ CSRFトークン取得
        token = driver.find_element(By.NAME, "token").get_attribute("value")
        print("🛡 CSRFトークン取得:", token)

        # ✅ ログインフォーム入力
        driver.find_element(By.NAME, "partner[email]").send_keys("kenou-akimoto@a2gjpn.co.jp")
        driver.find_element(By.NAME, "partner[password]").send_keys("kenouestate2024")

        # ✅ トークンを念のため再代入（JSで）
        driver.execute_script(f'document.getElementsByName("token")[0].value = "{token}"')

        # ✅ ログインボタンを押下
        driver.find_element(By.NAME, "commit").click()
        print("🔐 ログインボタン押下")
        time.sleep(2)

        # ✅ 顧客ページへ遷移
        driver.get(url)
        print("📦 顧客ページへ遷移:", driver.current_url)
        time.sleep(2)

        # ✅ HTMLデバッグログ
        print("📸 現在のURL:", driver.current_url)
        print("🧱 HTMLの冒頭:", driver.page_source[:1000])

        # ✅ XPathで情報抽出（まだ仮のまま）
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
