# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 18:18:39 2023

@author: fujii masaki
"""
from flask import Flask, render_template,request, session, redirect, url_for, abort
from youtubeapi import youtube_search
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# 標準ライブラリ
import os
from datetime import date, datetime, timedelta
#youtubeapiを使えるようにする
app = Flask(__name__)
app.secret_key = "abc"

# ========== spreadsheet 関連 ==========
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("./my-test-387105-4977250124a8.json", scope)  # <-このPATHの部分にjsonの鍵ファイル
client = gspread.authorize(creds)

# ユーザーデータ取得
USER_SHEET_KEY = "d/1r2-9rNK0myE8xLe0WPDSdz0LjU8MTBDfC7oiqhIaiw8/"  # <- ここにシートのURLを入れる
sh_user = client.open_by_key(USER_SHEET_KEY)  # <- シートのオブジェクト


@app.route("/")
def login():
    # ログインしていたらリダイレクト
    if "tatsuki_apps_auth" in session:
        return redirect(url_for("index"))

    return render_template(f"index1.html",
                           error=request.args.get("error"))  # <- エラー発生時用


@app.route("/", methods=["POST"])
def login_post():
    # 入力された値を取得
    user_id = request.form["tatsuki_apps_id"]
    user_password = request.form["tatsuki_apps_password"]

    # ユーザー情報リストを取得
    user_data_list = sh_user.worksheet("user_data").get_all_values()[1:]
    print(user_data_list)

    for ud in user_data_list:
        if (user_id, user_password) == (ud[0], ud[1]):  # ログイン成功
            # セッションに保存
            session["tatsuki_apps_auth"] = True
            session["tatsuki_apps_id"] = ud[0]
            # session["tatsuki_apps_password"] = ud[1]
            session["tatsuki_apps_role"] = ud[2]

            return redirect(url_for("mypage", username=user_id))  # <- 自分のマイページに飛ばす

    else:  # ログイン失敗
        return redirect(url_for("login", error=1))

@app.route('/you2')
def index2():
    titles_smart,urls_smart=youtube_search('スマホ依存')
    #searchに検索したワード入れてそれを反映したリスト
    return render_template('index2.html',titles_smart=titles_smart,urls_smart=urls_smart)

    # videos2=youtube_search("スマホ依存")
    # return render_template('index2.html')

@app.route('/you3',methods=["POST"])
def index3():
    search = request.form['search']
    titles,urls=youtube_search(search)
    #searchに検索したワード入れてそれを反映したリスト
    return render_template('index3.html',titles=titles,urls=urls)

@app.route('/you4')
def index4():
    return render_template('index4.html')        

if __name__ == "__main__":
    app.run(debug=True)