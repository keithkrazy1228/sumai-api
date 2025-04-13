from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_customer_info(url):  # Zapierから送られるURLは使わずOK
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # ログインページへ
        driver.get("https://sumai-step.com/partner/login")

        # ログイン情報入力
        driver.find_element(By.NAME, "partner[email]").send_keys("kenou-akimoto@a2gjpn.co.jp")
        driver.find_element(By.NAME, "partner[password]").send_keys("kenouestate2024")
        driver.find_element(By.NAME, "commit").click()

        # ログイン完了待ち（目印になるメニューを探す）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "side"))
        )

        # 反響一覧ページへ移動（ロビー）
        driver.get("https://sumai-step.com/partner/conversions")

        # ページが表示されるまで待機
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))  # ページ内にある何かしらの要素で待機
        )

        # ✅ ここが追加された部分！HTMLの中身をログに出力（短く）
        print("📸 現在のURL:", driver.current_url)
        print("🧱 HTMLの最初:", driver.page_source[:1000])  # HTML全体は長いので一部だけ

        # ロビー写真を撮影（HTML取得）
        return {"html": driver.page_source}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
