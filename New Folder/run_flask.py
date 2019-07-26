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

@app.route('/CheckCamera2')
def checkcam():
   with open('check.ck', 'rb') as file:
      check = pickle.load(file)
      print(check)
      return check

if __name__ == '__main__':
   app.debug = True
   check = 'Null'
   with open('check.ck', 'wb') as file:
      pickle.dump(check, file)
   app.run(host="0.0.0.0", threaded=True, port=80)



