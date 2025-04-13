from flask import Flask, request, jsonify
from selenium処理 import get_customer_info  # ここはあなたの関数名そのままでOK

app = Flask(__name__)

@app.route("/get-info", methods=["POST"])
def get_info():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        result = get_customer_info(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
