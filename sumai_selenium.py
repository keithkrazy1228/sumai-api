from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_customer_info(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"  # Render用Chromeパス

    service = Service(executable_path="/usr/bin/chromedriver")  # Render用Driverパス
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # ログインページへ
        driver.get("https://sumai-step.com/partner/login")

        # ログインフォーム入力
        driver.find_element(By.NAME, "partner[email]").send_keys("kenou-akimoto@a2gjpn.co.jp")
        driver.find_element(By.NAME, "partner[password]").send_keys("kenouestate2024")
        driver.find_element(By.NAME, "commit").click()

        # ログイン成功の確認（サイドメニューが出るまで待つ）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "side"))
        )

        # 顧客情報ページに遷移
        driver.get(url)

        # 顧客情報が表示されるまで待機
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="conversion_detail"]/div[1]/table/tbody/tr[1]/td'))
        )

        # 情報抽出
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
