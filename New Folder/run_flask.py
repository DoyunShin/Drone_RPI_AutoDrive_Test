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

#debug

@app.route('/dbg/index.html')
def dbg_main():
   return render_template("debug.html")

@app.route('/dbg/exit/true')
def dbg_setexit_true():
   check = 'true'
   with open('exit.ck', 'wb') as file:
      pickle.dump(check, file)
      return "changed", check

@app.route('/dbg/exit/false')
def dbg_setexit_false():
   check = 'false'
   with open('exit.ck', 'wb') as file:
      pickle.dump(check, file)
      return "changed", check

@app.route('/dbg/person/false')
def dbg_setperson_false():
   check = 'false'
   with open('person.ck', 'wb') as file:
      pickle.dump(check, file)
      return "changed", check

@app.route('/dbg/person/true')
def dbg_setperson_true():
   check = 'false'
   with open('person.ck', 'wb') as file:
      pickle.dump(check, file)
      return "changed", check

@app.route('/dbg/status/false')
def dbg_setstatus_false():
   check = 'false'
   with open('status.ck', 'wb') as file:
      pickle.dump(check, file)
      return "changed",check

@app.route('/dbg/status/true')
def dbg_setstatus_true():
   check = 'true'
   with open('status.ck', 'wb') as file:
      pickle.dump(check, file)
      return "changed",check


@app.route('/dbg/exit/look')
def dbg_checkexit():
   with open('exit.ck', 'rb') as file:
      check = pickle.load(file)
      print(check)
      return check

@app.route('/dbg/status/look')
def dbg_checkstatus():
   with open('status.ck', 'rb') as file:
      check = pickle.load(file)
      print(check)
      return check


@app.route('/dbg/person/look')
def dbg_checkperson():
   with open('person.ck', 'rb') as file:
      check = pickle.load(file)
      print(check)
      return check


#debug end

@app.route('/runexit')
def setexit_true():
   check = 'true'
   with open('exit.ck', 'wb') as file:
      pickle.dump(check, file)
      return check
 

@app.route('/checkexit')
def checkexit():
   with open('exit.ck', 'rb') as file:
      check = pickle.load(file)
      print(check)
      return check

@app.route('/checkstatus')
def checkstatus():
   with open('status.ck', 'rb') as file:
      check = pickle.load(file)
      print(check)
      return check


@app.route('/checkperson')
def checkperson():
   with open('person.ck', 'rb') as file:
      check = pickle.load(file)
      print(check)
      return check

if __name__ == '__main__':
   app.debug = True
   check = 'Null'
   with open('person.ck', 'wb') as file:
      pickle.dump(check, file)
   with open('status.ck', 'wb') as file:
      pickle.dump(check, file)
   with open('exit.ck', 'wb') as file:
      pickle.dump(check, file)
   app.run(host="0.0.0.0", threaded=True, port=80)

