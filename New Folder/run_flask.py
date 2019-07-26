from flask import *
from flask_compress import Compress
import os
import pickle

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.route('/')
def main():
   return render_template("main.html")

@app.route('/checktrue', methods = ['POST', 'GET'])
def checktrue():
   check = 'True'
   if request.method == 'POST':
      with open('check.ck', 'wb') as file:
         pickle.dump(check, file)
         return check
   else:
      with open('check.ck', 'wb') as file:
         pickle.dump(check, file)
      return check

@app.route('/checkfalse', methods = ['POST', 'GET'])
def checkfalse():
   check = "False"
   if request.method == 'POST':
      with open('check.ck', 'wb') as file:
         pickle.dump(check, file)
      return check
   else:
      with open('check.ck', 'wb') as file:
         pickle.dump(check, file)
      return check


@app.route('/CheckCamera2')
def checkcam():
   with open('check.ck', 'rb') as file:
      check = pickle.load(file)
      print(check)
   return check

if __name__ == '__main__':
   app.debug = True
   check = 'Null'
   app.run(host="0.0.0.0", threaded=True, port=80)



