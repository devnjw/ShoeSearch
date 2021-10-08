from flask import Flask, render_template, request, flash, redirect, url_for
import json
import requests
from .config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)

@app.route('/')
def home():
   keyword = request.args.get('keyword')
   if not keyword:
      keyword = ""

   url = 'http://127.0.0.1:5050/search?keyword=' + keyword
   res = requests.get(url).json()

   return render_template('result.html', items=res['data'])

@app.route('/search')
def string_search():
   keyword = request.args.get('keyword')
   if not keyword:
      keyword = ""

   url = 'http://127.0.0.1:5050/search?keyword=' + keyword
   res = requests.get(url).json()

   return render_template('result.html', items=res['data'])

@app.route('/image', methods=['POST'])
def image_search():
   file = request.files['file']

   if not file:
      flash("이미지 검색을 사용하려면, 이미지를 넣어주세요.\\nPlease put the image in for image search.")
      return render_template('index.html')   

   else:
      url = "http://127.0.0.1:5050/search/image"
      files = {'file': file}
      res = requests.post(url, files=files).json()

      return render_template('result.html', items=res['data'])

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=5000)