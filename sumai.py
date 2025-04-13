from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# ✅ ChromeDriverのパス（kenouさんの環境に合わせて指定済）
service = Service("C:/Users/kenou/Dropbox/PC/Documents/Ctools/chromedriver.exe")

# ✅ ヘッドレスChrome起動オプション
options = Options()
options.add_argument('--headless')  # ←必要ならコメントアウトで画面表示可
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# ✅ Chrome起動
driver = webdriver.Chrome(service=service, options=options)

try:
    # ① ログインページにアクセス
    driver.get("https://sumai-step.com/partner/login")
    time.sleep(2)

    # ② ログイン情報入力
    driver.find_element(By.ID, "partner_email").send_keys("kenou-akimoto@a2gjpn.co.jp")
    driver.find_element(By.ID, "partner_password").send_keys("kenouestate2024")
    driver.find_element(By.NAME, "commit").click()
    time.sleep(3)

    # ③ 反響一覧ページへ移動
    driver.get("https://sumai-step.com/partner/conversions")
    time.sleep(3)

    # ④ 一番上の反響リンク（反響日時）をクリック
    first_link = driver.find_element(By.CSS_SELECTOR, "table tbody tr td a")
    first_link.click()
    time.sleep(3)

    # ⑤ 顧客詳細ページのHTMLを確認（省略可）
    html = driver.page_source
    print("✅ 顧客詳細ページにアクセス成功！")

    # ⑥ 顧客情報のラベルと値を取得して表示
    labels = driver.find_elements(By.CLASS_NAME, "assessment-request__label")
    values = driver.find_elements(By.CLASS_NAME, "assessment-request__value")

    print("\n📋 顧客情報一覧：")
    for label, value in zip(labels, values):
        print(f"{label.text.strip()} ： {value.text.strip()}")

finally:
    # ⑦ ブラウザを閉じる
    driver.quit()
