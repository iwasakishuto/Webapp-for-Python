from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flaskr.db import init_db
# from flaskr.seeds import setup_seeds
from flask_migrate import Migrate
from datetime import datetime
import smtplib  # Gmail
import slackweb # Slack
import requests # LINE

#=== Flaskアプリを作成 ===
app = Flask(__name__)
# SQLiteを使用する。プロジェクトフォルダにあるdbサブフォルダの下にあるsample.dbファイルをデータベースとして利用。
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# Warnig が出るのが面倒なので、消しておく。（本筋には無関係）
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# SQLAlchemyクラスのコンストラクタに渡して、インスタンスを作成
db = SQLAlchemy(app)
# アプリケーションで使うデータベースの定義を自動的に作成・管理する
migrate = Migrate(app, db)

#=== Line notify を利用 ===
line_notify_token = 'XXX' # LINEを送りたいグループのトークン
line_notify_api = 'https://notify-api.line.me/api/notify'
line_message = '〇〇くん！！肉じゃがと餃子がそろそろ賞味期限きれちゃうよ！！！気をつけて！（Hackathon用です。失礼しました笑）'

#=== Gmail ===
# Content
TO = 'XXX@gmail.com' # 江口
SUBJECT = 'From Delite'
TEXT = 'Hi!! 〇〇! You have to cook Gyoza, and Nikujaga ASAP.'

# Sign In
gmail_sender = 'YYY@gmail.com'
gmail_passwd = 'PASS'
BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])
#=== Slack ===
slack_url = "https://hooks.slack.com/services/XXX"
slack = slackweb.Slack(url=slack_url)

# 普段の処理
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register')
def register():
  return render_template('Registration.html')

# 会員登録
@app.route('/creat_account', methods=['GET','POST'])
def creat_account():
  if request.method == 'POST':
    # 登録フォームから値を受け取って、データベースに接続する。
    username = request.form["username"]
    password = request.form["password"]
    email    = request.form["email"]
    print()
    print("creat username: {}".format(username))
    print("creat password: {}".format(password))
    print("creat email   : {}".format(email))
    print()
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
  return render_template('index.html')

# ログイン
@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    # 入力した内容と一致しているかを見る。
    username = request.form["username"]
    password = request.form["password"]
    print("login username: {}".format(username))
    print("login password: {}".format(password))
    # データベースから username の等しいアカウントを取得する。
    user = db.session.query(User).filter_by(username=username)[-1]
    # 登録されており、パスワードが等しかったら、Mypage に遷移する。
    print("dbからのデータ{}".format(user))
    print("名前: {}".format(user.username))
    print("パスワード: {}".format(user.password))
    if user and user.password == password:
      return render_template('profile-page.html', contribution="0", stock="3", route="0", before="1")
  return render_template('index.html')

@app.route('/send', methods=['GET','POST'])
def send():
    #=== Gmail ===
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')
    server.quit()

    #=== Slack ===
    slack.notify(text="こら！ <@XXX> 肉じゃがと餃子を作りなさいって言ったじゃないの！！もう、しょうがないんだから。今から作りに行くから待っててね！！")

    #=== LINE ===
    line_payload = {'message': line_message}
    line_headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    line_notify = requests.post(line_notify_api, data=line_payload, headers=line_headers)
    return render_template('profile-page.html')

# ログイン
@app.route('/evaluate', methods=['GET','POST'])
def evaluate():
    if request.method == 'POST':
        return render_template('profile-page.html', contribution="1", stock="2", route="1")

# パスタの料理ページへの遷移用。
@app.route('/pasta')
def pasta():
    return render_template('recipe.html')

## Models
class User(db.Model): # モデルの基底クラス。
  __tablename__ = 'users' # テーブルの名前
  #=== カラムの定義 ===
  id = db.Column(db.Integer, primary_key=True, nullable=False)
  username = db.Column(db.String(255), nullable=False)
  password = db.Column(db.String(80), unique=False, nullable=False)
  email = db.Column(db.String(80), unique=False, nullable=False)
  household_size = db.Column(db.Integer, unique=False, nullable=False, default=1)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  hate_meals = db.relationship('HateMeal', backref='user', lazy=True)
  current_meals = db.relationship('UserMealsCooked', backref='user', lazy=True)
  allergies = db.relationship('Allergy', backref='user', lazy=True)

class HateMeal(db.Model):
  __tablename__ = 'hate_meals'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)

class Meal(db.Model):
  __tablename__ = 'meals'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  title = db.Column(db.String(80), nullable=False)
  how_to_cook = db.Column(db.String(255), nullable=False)
  image_url = db.Column(db.String(255), nullable=True)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class UserMealsCooked(db.Model):
  __tablename__ = 'user_meals_cooked'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  cooked = db.Column(db.Boolean, nullable=False, default=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)

class Allergy(db.Model):
  __tablename__ = 'allergies'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

if __name__ == "__main__":
  init_db(app)    # データベースを作成。
  db.create_all() # データベース構造を最初に作る。
  # setup_seeds()
  app.run(debug=True)
