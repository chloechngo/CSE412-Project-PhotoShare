import os, base64
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
import flask_login
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 
import datetime

#for image uploading
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage




mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'cse_412'  # Change this later


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'chloengo' 
app.config['MYSQL_DATABASE_DB'] = 'CSE412Schema'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

#----------Login---------------
login_manager = LoginManager()
login_manager.init_app(app)

connection= mysql.connect()
cur = connection.cursor()
cur.execute("SELECT email from Users") 
users = cur.fetchall()

# use Flask's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
	pass

@app.route('/')
@login_required
def authorized():
    return 'Authenticated users only!'




@login_manager.request_loader
def custom_request_loader(request):
	users = get_user_list()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	currentuser = User()
	currentuser.id = email
	cur = mysql.connect().cursor()
	cur.execute("SELECT hashed_password FROM Users WHERE email = '{0}'".format(email))
	data = cur.fetchall()
	passwords = str(data[0][0])
	currentuser.is_authenticated = request.form['password'] == passwords
	return currentuser

@login_manager.user_loader
def custom_user_loader(email):
	currentuser = get_user_list()
	if not(email) or email not in str(currentuser):
		return
	currentuser = User()
	currentuser.id = email
	return currentuser


def get_user_list():
	cur = connection.cursor()
	cur.execute("SELECT email from Users") 
	return cur.fetchall()

def unique_email(email):
	cur = connection.cursor()
	if cur.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)): 
		return False
	else:
		return True

def usrid_from_email(email):
	cur = connection.cursor()
	cur.execute("SELECT user_id FROM Users WHERE email = '{0}'".format(email))
	return cur.fetchone()[0]

def usrname_from_email(email):
	cur = connection.cursor()
	cur.execute("SELECT first_name FROM Users WHERE email = '{0}'".format(email))
	return cur.fetchone()[0]

def usr_info():
	email = flask_login.current_user.id
	cur = connection.cursor()
	cur.execute("SELECT * FROM Users WHERE email = '{0}'".format(email))
	return cur.fetchone()

def albid_from_albname(album_name):
	cur = connection.cursor()
	cur.execute("SELECT album_id FROM Album WHERE album_name = '{0}'".format(album_name))
	return cur.fetchone()[0]

def top_ten_usr():
	cur = connection.cursor()
	cur.execute("SELECT * FROM Users ORDER BY contribution DESC LIMIT 10")
	return cur.fetchall()

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('home.html') 

@app.route('/account')
@flask_login.login_required
def account():
	userInfo = usr_info()
	return render_template('account.html', userInfo=userInfo)

@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html', supress='True') 

@app.route("/register", methods=['POST'])
def signed_up_usr():
    try:
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['firstn']
        last_name = request.form['lastn']
        date_of_birth = request.form['dateofbirth']
        hometown = request.form['hometown']
        gender = request.form['gender']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (email, hashed_password, first_name, last_name, date_of_birth, gender, hometown) VALUES (%s, %s, %s, %s, %s, %s, %s)", (email, password, first_name, last_name, date_of_birth, gender, hometown))
        mysql.connection.commit()
        cur.close()
        
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
        
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('register'))
    


@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return render_template('login.html')



	
	email = flask.request.form['email']
	cur = connection.cursor()
	if cur.execute("SELECT hashed_password FROM Users WHERE email = '{0}'".format(email)):
		data = cur.fetchall()
		pwd = str(data[0][0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) 
			return flask.redirect(flask.url_for('authorized')) 
	return render_template('login.html', message="Incorrect email or password. Please check again!")

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return render_template('home.html', message='Logged out') 


if __name__ == "__main__":
    # this is invoked when in the shell you run
    # $ python app.py
    app.run(port=5500, debug=True)