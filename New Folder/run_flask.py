from flask import *
from flask_compress import Compress
import os


compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/checktrue', methods = ['POST', 'GET'])
def checktrue():
   if request.method == 'POST':
      check = 'True'
      return check
   else:
      check = 'True'
      return check

@app.route('/checkfalse', methods = ['POST', 'GET'])
def checkfalse():
   if request.method == 'POST':
      check = 'false'
      return check
   else:
      check = 'false'
      return check


@app.route('/CheckCamera2')
def checkcam():
    return check


if __name__ == '__main__':
    app.debug = True
    check = 'False'
    app.run(host="0.0.0.0", threaded=True, port=80)



