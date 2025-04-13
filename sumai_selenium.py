from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_customer_info(url):
    # Chromeオプション設定（ヘッドレス推奨）
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # chromedriverパス（Render用には別途設定が必要なことも）
    service = Service(executable_path="chromedriver")  # ローカルならパス明記

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # ① ログインページにアクセス
        driver.get("https://sumai-step.com/partner/login")
        time.sleep(2)

        # ② ログインフォーム入力（IDとPW）
        driver.find_element(By.NAME, "partner[email]").send_keys("kenou-akimoto@a2gjpn.co.jp")
        driver.find_element(By.NAME, "partner[password]").send_keys("kenouestate2024")
        driver.find_element(By.NAME, "commit").click()
        time.sleep(2)

        # ③ URLを開く（顧客詳細ページ）
        driver.get(url)
        time.sleep(2)

        # ④ 情報を抽出（例：名前・住所など）
        name = driver.find_element(By.XPATH, '//*[@id="conversion_detail"]/div[1]/table/tbody/tr[1]/td').text
        address = driver.find_element(By.XPATH, '//*[@id="conversion_detail"]/div[1]/table/tbody/tr[2]/td').text
        tel = driver.find_element(By.XPATH, '//*[@id="conversion_detail"]/div[1]/table/tbody/tr[3]/td').text

        return {
            "name": name,
            "address": address,
            "tel": tel
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
