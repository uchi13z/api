from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime
import pytz  # pytzライブラリをインポート

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_stock_price():
    ticker = "4902.T"
    stock = yf.Ticker(ticker)
    
    # 最新の1日データを取得
    history = stock.history(period="1d")
    if history.empty:
        return jsonify({"error": "No data found"}), 404

    latest = history.iloc[-1]
    
    # 現在のマーケットデータを取得
    try:
        current_price = stock.info.get('currentPrice', None)
        open_price = stock.info.get('regularMarketOpen', latest.get('Open', None))
        high_price = stock.info.get('dayHigh', latest.get('High', None))
        low_price = stock.info.get('dayLow', latest.get('Low', None))
        close_price = stock.info.get('previousClose', latest.get('Close', None))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # タイムスタンプを日本標準時に変換
    jst = pytz.timezone('Asia/Tokyo')
    timestamp = datetime.now(pytz.utc).astimezone(jst).strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "symbol": ticker,
        "timestamp": timestamp,
        "open": open_price,
        "close": close_price,
        "high": high_price,
        "low": low_price,
        "current": current_price
    }

    return jsonify(data)

@app.route('/health')
def health():
    return jsonify(status='healthy'), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
