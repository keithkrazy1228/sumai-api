import requests
from bs4 import BeautifulSoup

# ✅ アカウント情報（Tom用）
ID = "kenou-tomita@a2gjpn.co.jp"
PASSWORD = "kenouestate2024"

# ✅ セッション & ヘッダー設定
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://sumai-step.com/partner/sign_in"
}

# ✅ 1. ログインページ取得
login_url = "https://sumai-step.com/partner/sign_in"
response = session.get(login_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# ✅ 2. トークン取得
token_tag = soup.find("input", {"name": "authenticity_token"})
if not token_tag:
    print("❌ CSRFトークンが見つかりません。")
    exit()

token = token_tag.get("value")

# ✅ 3. ログイン用データ構築（ID/PW入り）
payload = {
    "utf8": "✓",
    "partner[email]": "kenou-tomita@a2gjpn.co.jp",
    "partner[password]": "kenouestate2024",
    "authenticity_token": token,
    "commit": "ログイン"
}

# ✅ 4. ログイン実行
login = session.post(login_url, data=payload, headers=headers)

# ログイン判定
if "ログインしてください" in login.text:
    print("❌ ログインに失敗しました。")
    exit()
else:
    print("✅ ログイン成功")

# ✅ 5. 反響一覧ページにアクセス
list_url = "https://sumai-step.com/partner/conversions"
res = session.get(list_url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# ✅ 6. 顧客詳細リンクを抽出（先頭1件）
link_tag = soup.find("a", href=lambda href: href and href.startswith("/partner/conversions/CO"))
if not link_tag:
    print("❌ 顧客詳細ページリンクが見つかりません。")
    exit()

detail_url = "https://sumai-step.com" + link_tag["href"]
print("🔗 顧客詳細ページURL:", detail_url)

# ✅ 7. 顧客詳細ページにアクセス
detail_res = session.get(detail_url, headers=headers)

if "ログインしてください" in detail_res.text:
    print("❌ 顧客ページ取得失敗（ログアウト状態）。")
    exit()
else:
    print("✅ 顧客ページ取得成功！")

# ✅ 8. 顧客ページHTML（冒頭のみ表示）
print("\n🧾 顧客ページHTML冒頭（1000文字）:")
print(detail_res.text[:1000])
