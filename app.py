from flask import Flask, render_template,request,session,url_for,redirect
from flask_mysqldb import MySQL,MySQLdb,cursors
import pickle
import numpy as np
import mysql.connector
import re
import mysql
import stripe
import pandas as pd








model = pickle.load(open('f.pkl', 'rb'))


app = Flask(__name__)
YOUR_DOMAIN="http://locahost:5000"
app.secret_key="King"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='user_system'
mysql=MySQL(app)
public_key = "pk_test_6pRNASCoBOKtIshFeQd4XMUh"
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"


    





@app.route('/')
def man():
    return render_template('home.html')
@app.route('/sign',methods=['GET','POST'])
def sign():
   mesage =''

   if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not name or not email or not password:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (name, email, password ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
   elif request.method == 'POST':
        mesage = 'Please fill out the form !'
   return render_template('sign.html', mesage = mesage)


@app.route('/buy')
def buy():

    return render_template('buy.html')
@app.route('/payment')
def payment():
       return render_template("checkout.html",public_key=public_key)


@app.route('/purchase',methods=['POST'])
def purchase():
      
     customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                        source=request.form['stripeToken'])
     charge = stripe.Charge.create(
            customer=customer.id,
            amount = 210,
            currency = 'Tk',
            description = 'CROP Payment',
      )
     return redirect(url_for('thankyou'))




  
   

@app.route('/login',methods=['GET','POST'])
def login():

    mesage=''
    if request.method=='POST' and 'email' in request.form and 'password' in request.form:
        
        email = request.form['email']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email =%s AND password=%s',(email,password) )
        user = cursor.fetchone()
        if user:
            session['loggedin']=True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage='Logged in successfully !'
            return render_template('user.html',mesage=mesage)
        else:
            mesage='Please enter correct email/password!'
    return render_template('login.html')



@app.route('/predict', methods=['POST'])
def home():
    data1 = request.form['N']
    data2 = request.form['P']
    data3 = request.form['K']
    data4 = request.form['temperature']
    data5 = request.form['humidity']
    data6 = request.form['ph']
    data7 = request.form['rainfall']
    arr = np.array([[data1, data2, data3, data4,data5,data6,data7]])
    pred = model.predict(arr)
    return render_template('after.html', data=pred)
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
@app.route('/fertilizer')
def fertilizer():
    return render_template('fertilizer.html')


if __name__ == "__main__":
    app.run(debug=True)















