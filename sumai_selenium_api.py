from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# === サンプルのルート ===
@app.route("/", methods=["GET"])
def index():
    return "Sumai Step API is running!"

# === 任意のAPIエンドポイント ===
@app.route("/api/get_customer_info", methods=["POST"])
def get_customer_info():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    # ここでSelenium処理を実行
    result = {
        "url": url,
        "status": "Selenium処理実行予定（ここにロジックを入れてください）"
    }
    return jsonify(result)

# === ポートバインドの修正点ここ！ ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
