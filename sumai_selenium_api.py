from flask import Flask, request, jsonify
from sumai_selenium import get_customer_info  # 外部の処理ファイルから読み込み

app = Flask(__name__)

@app.route("/get-info", methods=["POST"])
def get_info():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = get_customer_info(url)
    return jsonify(result)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
