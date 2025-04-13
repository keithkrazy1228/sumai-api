from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# すまいステップのログインURL
LOGIN_URL = "https://sumai-step.com/partner/login"
ID = "kenou-akimoto@a2gjpn.co.jp"
PASSWORD = "kenouestate2024"

@app.route('/')
def home():
    return "Sumai Step BS API is live!"

@app.route('/api/get_customer_info', methods=['POST'])
def get_customer_info():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "Missing 'url' in request"}), 400

        # セッション開始
        session = requests.Session()

        # Step 1: CSRFトークン取得
        resp = session.get(LOGIN_URL)
        soup = BeautifulSoup(resp.text, "html.parser")
        token_input = soup.find("input", {"name": "authenticity_token"})
        token = token_input.get("value") if token_input else ""

        headers = {
            "Referer": LOGIN_URL,
            "Origin": "https://sumai-step.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/x-www-form-urlencoded"
        }

       payload = {
    "partner[email]": "kenou-akimoto@a2gjpn.co.jp",
    "partner[password]": "kenouestate2024",
    "authenticity_token": token
}

        # Step 2: ログイン
        resp_login = session.post(LOGIN_URL, data=payload, headers=headers)
        if "ログインしてください" in resp_login.text:
            return jsonify({"error": "Login failed."}), 401

        # Step 3: 顧客情報ページ取得
        resp_detail = session.get(url)
        soup = BeautifulSoup(resp_detail.text, "html.parser")

        # Step 4: データ抽出
        data_map = {}
        rows = soup.select("table tr")
        for row in rows:
            label_cell = row.select_one("td.assessment-request_label")
            value_cell = row.select_one("td.assessment-request_value")
            if label_cell and value_cell:
                label = label_cell.text.strip()
                value = value_cell.text.strip()
                data_map[label] = value

        result = {
            "管理番号": data_map.get("\u7ba1\u7406\u756a\u53f7", ""),
            "反響日時": data_map.get("\u53cd\u97ff\u65e5\u6642", ""),
            "物件住所": data_map.get("\u7269件住所", ""),
            "氏名": data_map.get("\u6c0f名", ""),
            "電話番号": data_map.get("\u96fb話番号", ""),
            "メールアドレス": data_map.get("\u30e1ールアドレス", "")
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
