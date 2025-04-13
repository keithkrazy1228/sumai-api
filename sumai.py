from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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

        session = requests.Session()

        # Step 1: GET login page to fetch authenticity_token
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
            "partner[email]": ID,
            "partner[password]": PASSWORD,
            "authenticity_token": token
        }

        # Step 2: POST login form
        resp_login = session.post(LOGIN_URL, data=payload, headers=headers)
        if "ログインしてください" in resp_login.text:
            return jsonify({"error": "Login failed."}), 401

        # Step 3: GET customer page
        resp_detail = session.get(url)
        soup = BeautifulSoup(resp_detail.text, "html.parser")

        # Step 4: Extract data
        try:
            rows = soup.select("#conversion_detail table tr")
            name = rows[0].select_one("td").text.strip()
            address = rows[1].select_one("td").text.strip()
            tel = rows[2].select_one("td").text.strip()
        except Exception as e:
            return jsonify({"error": f"Failed to parse customer data: {str(e)}"}), 500

        return jsonify({
            "name": name,
            "address": address,
            "tel": tel
        })

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
