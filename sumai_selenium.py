def get_customer_info(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 🟡 ここだけ変更：会社HPを直接開く
        driver.get("https://renovation.a2gjpn.co.jp/")  # ←会社のURLに変更！

        # ✅ ページが開くのを確認（ページタイトルなど）
        print("📸 URL:", driver.current_url)
        print("🧱 HTML前半:", driver.page_source[:1000])  # HTMLの冒頭を出力

        return {"html": driver.page_source}

    except Exception as e:
        print("❌ ERROR:", e)
        return {"error": str(e)}

    finally:
        driver.quit()
