from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# ✅ 正しいログイン情報（Tom用）
EMAIL = "kenou-akimoto@a2gjpn.co.jp"
PASSWORD = "kenouestate2024"

# ✅ ChromeDriver のパス（Tomの環境に合わせてある）
CHROMEDRIVER_PATH = "C:\\Users\\kenou\\Dropbox\\PC\\ドキュメント\\Ctools\\chromedriver.exe"

# ✅ Chrome起動オプション
options = Options()
# options.add_argument("--headless")  # 今回は「画面表示あり」でSeleniumブロック回避
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# ✅ ドライバ起動
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. ログインページへアクセス
    driver.get("https://sumai-step.com/partner/sign_in")
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    time.sleep(2)

    # 2. ログイン情報入力
    driver.find_element(By.NAME, "partner[email]").send_keys("kenou-akimoto@a2gjpn.co.jp")
    driver.find_element(By.NAME, "partner[password]").send_keys("kenouestate2024")

    # 3. ログインボタン押下
    driver.find_element(By.NAME, "commit").click()
    time.sleep(3)

    # 4. 反響一覧ページへ移動（ここでもJSブロック解除スクリプトを再注入）
    driver.get("https://sumai-step.com/partner/conversions")
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    time.sleep(3)

    # 5. 顧客詳細リンクを取得し、clickせず直接GET
    link = driver.find_element(By.CSS_SELECTOR, 'a[href^="/partner/conversions/CO"]')
    detail_url = link.get_attribute("href")
    print("🔗 顧客詳細ページURL:", detail_url)

    driver.get(detail_url)  # ← clickではなく直接アクセス
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    time.sleep(3)

    # 6. 顧客ページのHTMLを取得して冒頭を表示
    html = driver.page_source
    print("✅ 顧客ページ取得成功！HTML冒頭:")
    print(html[:1500])

except Exception as e:
    print("❌ エラーが発生しました:", e)

finally:
    driver.quit()
