import requests
from bs4 import BeautifulSoup

ID = "kenou-tomita@a2gjpn.co.jp"
PASSWORD = "kenouestate2024"

session = requests.Session()

login_url = "https://sumai-step.com/partner/sign_in"
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")

token = soup.find("input", {"name": "authenticity_token"}).get("value")

payload = {
    "partner[email]": "kenou-tomita@a2gjpn.co.jp",
    "partner[password]": "kenouestate2024",
    "authenticity_token": token
}


headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": login_url
}

login = session.post(login_url, data=payload, headers=headers)

print("ログイン後URL:", login.url)
print("ログイン後ステータス:", login.status_code)
print("ログイン後HTML冒頭:", login.text[:300])  # ←ここで「ログインしてください」が出てないか確認

# 顧客ページアクセス
target_url = "https://sumai-step.com/partner/conversions/CO2504-XXXX"
res = session.get(target_url, headers=headers)

print("顧客ページ冒頭:", res.text[:300])
