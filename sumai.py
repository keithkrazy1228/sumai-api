import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://sumai-step.com/partner/login"
TARGET_URL = "https://sumai-step.com/partner/conversions/CO2504-76152"

ID = "kenou-akimoto@a2gjpn.co.jp"
PASSWORD = "kenouestate2024"

session = requests.Session()

# ログインページ取得
resp = session.get(LOGIN_URL)
soup = BeautifulSoup(resp.text, "html.parser")
token_input = soup.find("input", {"name": "authenticity_token"})
token = token_input.get("value") if token_input else ""

# ログイン送信
payload = {
    "partner[email]": "kenou-akimoto@a2gjpn.co.jp",
    "partner[password]": "kenouestate2024",
    "authenticity_token": token
}


headers = {
    "Referer": LOGIN_URL,
    "Origin": "https://sumai-step.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/x-www-form-urlencoded"
}

resp_login = session.post(LOGIN_URL, data=payload, headers=headers)

print("🟡 ログイン後のページ冒頭:")
print(resp_login.text[:1000])

if "ログインしてください" in resp_login.text:
    print("❌ ログイン失敗")
    exit()
else:
    print("✅ ログイン成功！")

# 顧客ページアクセス
resp_data = session.get(TARGET_URL)
soup = BeautifulSoup(resp_data.text, "html.parser")

print("🧾 顧客ページHTML（冒頭）:")
print(soup.prettify()[:2000])
