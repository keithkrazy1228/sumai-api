from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_customer_info(url):  # Zapierから送られるurlは無視してOK
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # ✅ 軽いテスト用サイトを開く
        driver.get("https://httpbin.org/html")
        time.sleep(2)  # ページ描画待ち

        # ✅ HTMLの冒頭をログ出力（Renderのログで確認用）
        print("📸 URL:", driver.current_url)
        print("🧱 HTML冒頭:", driver.page_source[:1000])

        # ✅ Zapierにも返す（中身が見られる）
        return {"html": driver.page_source}

    except Exception as e:
        print("❌ ERROR:", e)
        return {"error": str(e)}

    finally:
        driver.quit()
