# coding: utf-8
from flask import Flask, request, render_template

model = "MODEL"
app = Flask(__name__) # 初期化(インスタンスとして生成)

#=== 通常時('/'にアクセスがきた時)の処理 ===
@app.route('/')
def index():
    return render_template('index.html')

#=== 画像がアップロードされた時('/send'にアクセスがきた時)の処理 ===
@app.route('/send', methods=['POST'])
def send():
    x = request.files['image']
    """
    〜〜色々処理〜〜
    """
    prediction = model.predict(x) # prediction は、string型とか。
    return render_template('index.html', class_name=prediction)

if __name__=='__main__':
    app.run()
