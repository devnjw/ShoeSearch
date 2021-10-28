from flask import Flask, render_template, request, flash, redirect, url_for
import json
import requests

app = Flask(__name__)

@app.route('/', methods=['get'])
def image_search():
    url = "http://127.0.0.1:5050/admin/image"
    res = requests.get(url).json()

    return render_template('result.html', items=res['data'])

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=1902)