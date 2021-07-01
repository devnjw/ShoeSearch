from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
   url = 'http://127.0.0.1:5050/home'
   requests.get(url)

   return render_template('index.html')

@app.route('/result')
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

   url = "http://127.0.0.1:5050/search/image"
   files = {'file': file}
   res = requests.post(url, files=files).json()

   print(res)

   return render_template('result.html', items=res['data'])

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=9000)