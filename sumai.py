import requests
from bs4 import BeautifulSoup

ID = "xxx@example.com"
PASSWORD = "xxxxxxxx"

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


login = session.post(login_url, data=payload)

# ログイン後の反響ページへアクセス
target_url = "https://sumai-step.com/partner/conversions/CO2504-XXXX"
res = session.get(target_url)

print(res.text)
