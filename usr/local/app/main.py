# coding: utf-8
from selenium_chrome import SeleniumChrome
from flask import Flask, render_template, send_file, request

chrome = SeleniumChrome()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def form():
    email    = request.form["email"]
    password = request.form["password"]
    form_url = request.form["form_url"]
    chrome.loginGoogleAccount(email, password)
    formkwargs = {
        "email": email,
        "number": 2929292929,
        "text": "お肉が食べたいです。",
    }
    filename = chrome.ansGoogleForm(form_url, screenshot=True, **formkwargs)
    return send_file(filename, mimetype='image/png')

if __name__ == "__main__":
    app.run()
