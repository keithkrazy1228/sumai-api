FROM python:3.11-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    chromium \
    chromium-driver \
    && apt-get clean

# 環境変数設定（Seleniumがchromiumを見つけやすく）
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 作業ディレクトリ
WORKDIR /app

# ファイルをコピー
COPY . .

# Python依存インストール
RUN pip install --upgrade pip && pip install -r requirements.txt

# ポート指定（Render用）
ENV PORT 10000

# アプリ起動
CMD ["python", "sumai_selenium_api.py"]
