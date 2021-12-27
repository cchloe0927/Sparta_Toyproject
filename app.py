from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta_hj                   # 'dbsparta_hj'라는 이름의 db를 만듭니다.

@app.route('/')
def main():
   return render_template("index.html")

@app.route('/detail')
def detail():
   return render_template("detail.html")


# API 역할을 하는 부분
@app.route('/recommend', methods=['GET'])
def show_movies():
    movies = list(db.toymovies.find({}, {'_id': False}))    # .sort('star', -1))
    return jsonify({'recommend_movies': movies})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)