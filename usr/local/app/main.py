# coding: utf-8
import requests
from flask import Flask, redirect, request, render_template, url_for
from werkzeug.utils import secure_filename
from slackclient import SlackClient

#=== パラメタ ===
# OAuth Access
TOKEN       = "xoxp-000000000000-000000000000-000000000000-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# Bot User OAuth Access Token
BOT_TOKEN   = "xoxb-000000000000-000000000000-XXXXXXXXXXXXXXXXXXXXXXXX"
MESSAGE_URL = "https://slack.com/api/channels.history"
EMOJI_URL   = "https://slack.com/api/emoji.list"
FILE_URL    = "https://slack.com/api/files.upload"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])
#=== インスタンスの初期化 ===
app = Flask(__name__)
sc = SlackClient(BOT_TOKEN)

#=== ファイルのアップロード可否判定関数。２つの項目をチェックする。 ===
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#=== 普段の処理 ===
@app.route('/')
def index():
    return render_template('index.html')

#=== POSTで送られてきたテキストを受け取り、Slack APIを利用して送信する ===
@app.route('/send', methods=['POST'])
def send():
    #=== チャンネルの内容を見る場合 ===
    if request.form["button"] == "check":
        print("a")
        ch_id = request.form["Channe"] # フォームから選択されているチャンネル名を取得する。
        payload = {
            "channel": ch_id,
            "token": TOKEN
        }
        response = requests.get(MESSAGE_URL, params=payload)
        json_data = response.json()
        msgs = json_data['messages'] # テキストの内容のみを返している。
        return render_template('index.html',
         text1=msgs[5]["text"], ts1=msgs[5]["ts"],
         text2=msgs[4]["text"], ts2=msgs[4]["ts"],
         text3=msgs[3]["text"], ts3=msgs[3]["ts"],
         text4=msgs[2]["text"], ts4=msgs[2]["ts"],
         text5=msgs[1]["text"], ts5=msgs[1]["ts"],
         text6=msgs[0]["text"], ts6=msgs[0]["ts"],
         )
    #=== メッセージを送信する場合 ===
    else:
        ch_id = request.form["Channe"] # フォームから選択されているチャンネル名を取得する。
        text = request.form["text"] # フォームからテキスト内容を取得する。
        #=== 返信をする場合 ===
        if "reply" in request.form.keys():
            thread_ts = request.form["reply"]
            sc.api_call(
              "chat.postMessage",
              channel=ch_id,
              text=text,
              thread_ts=thread_ts,
            )
        #=== 単純にメッセージを送信する場合 ===
        else:
            sc.api_call(
              "chat.postMessage",
              channel=ch_id,
              text=text
            )
        return render_template('index.html', send=1) # 送信したことを伝えつつ、htmlを返す。

if __name__ == '__main__':
    app.run(debug=True)
