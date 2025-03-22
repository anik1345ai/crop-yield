from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__)
@app.route('/sign')
def sign():
    return render_template('sign.html')
if(__name__)==('__main__'):
    app.run(debug=True)