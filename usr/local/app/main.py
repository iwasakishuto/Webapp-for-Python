# coding: utf-8
from flask import Flask,render_template

# 初期化
app = Flask(__name__)

# ルートアクセス時の処理
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
