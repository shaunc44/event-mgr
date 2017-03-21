from flask import Flask, render_template, session, g, json, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import datetime
import os
# from werkzeug import generate_password_hash, check_password_hash #Do I need this anymore?


mysql = MySQL()
app = Flask(__name__, static_url_path='/static')
#Don't store the secret key this way (always store in separate)
app.secret_key = 'tobeornottobeasecretkey'
# app.secret_key = os.urandom(50)


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'shaun'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'event_mgr'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


app.config['UPLOAD_FOLDER'] = 'static/Uploads'


@app.route('/', methods = ['GET'])
def main():
	return render_template('index.html')


@app.route('/logOut')
def logOut():
	session.clear()
	return redirect('/')


#Do I need this anymore?
@app.route('/showUserPage')
def showUserPage():
	return render_template('user-page.html')


#Implement this later

# @app.route('/getPostsByUser')
# def getPostsByUser():
# 	try:
# 		if session.get('user_id'):
# 			_username = session.get('username')
# 			_user_id = session.get('user_id')

# 			con = mysql.connect()
# 			cursor = con.cursor()
# 			cursor.callproc('sp_getPostsByUser',(_user_id,))
# 			posts = cursor.fetchall()

# 			posts_dict = []
# 			for post in reversed(posts):
# 				print (type(post[2]))
# 				post_dict = {
# 					'Id': post[0],
# 					'Title': post[3],
# 					'Text': post[4],
# 					'Date': post[2].strftime("%a, %b %d, %Y")
# 				}
# 				posts_dict.append(post_dict)

# 			return json.dumps(posts_dict)
# 		else:
# 			return render_template('error.html', error = 'Unauthorized Access')
# 	except Exception as e:
# 		return render_template('error.html', error = str(e))


@app.route('/addUserEvent', methods=['POST'])
def addUserEvent():
	try:
		if session.get('user_id'):
			_user_id = session.get('user_id')
			_title = session['title']
			print (_user_id)
			print (_title)

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_getEventId',(_title,))
			_event = cursor.fetchone()
			_event_id = _event[0][0]
			print (_event)
			print (_event_id)
			cursor.close()
			conn.close()

			cursor.callproc('sp_addUserEvent',(_user_id, event_id))
			conn.commit()
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return redirect('/showUserPage')
			else:
				return render_template('error.html',error = 'An error occurred!')
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	else:
		cursor.close()
		conn.close()


@app.route('/addEvent', methods=['POST'])
def addEvent():
	try:
		if session.get('user_id'):
			# _user_id = session.get('user_id')
			_title = request.form['inputTitle']
			_description = request.form['inputDescription']
			_location = request.form['inputLocation']
			session['title'] = _title

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_addEvent',(_title, _description, _location))
			conn.commit()
			# cursor.callproc('sp_getEventId')
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				cursor.close()
				conn.close()
				return redirect('/showUserPage')
			else:
				return render_template('error.html',error = 'An error occurred!')
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	else:
		cursor.close()
		conn.close()


# @app.route('/getUsername')
# def getUsername():
# 	_username = session.get('username')
# 	uname = {
# 		'Username': _username
# 	}
# 	uname_dict =[]
# 	uname_dict.append(uname)
# 	return json.dumps(uname_dict)


# #This enters/verifies user info to/from the DB
@app.route('/signUp', methods=['POST','GET'])
def signUp():
	try:
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']

		# validate the email & password
		if _email and _password:
			# All Good, let's call MySQL
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_validateLogin',(_email,))
			data = cursor.fetchall()

			if len(data) > 0:
				if data[0][2] == _password:
					session['email'] = _email
					session['user_id'] = data[0][0]
					# session['password'] = data[0][1]
					cursor.close()
					conn.close()
					return redirect('/showUserPage')
				else:
					return render_template('error.html', error = 'Wrong Email address or Password')

			elif len(data) is 0:
				cursor.callproc('sp_createUser',(_email, _password))
				conn.commit()
				cursor.callproc('sp_validateLogin',(_email,))
				data = cursor.fetchall()
				session['email'] = _email
				session['user_id'] = data[0][0]
				cursor.close()
				conn.close()
				return redirect('/showUserPage')

			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	except Exception as e:
		return json.dumps({'error':str(e)})
	else:
		cursor.close()
		conn.close()


# #This just enters user info into the DB
# @app.route('/signUp', methods=['POST','GET'])
# def signUp():
# 	try:
# 		_username = request.form['inputUsername']

# 		# validate the received values
# 		if _username:
# 			# All Good, let's call MySQL
# 			conn = mysql.connect()
# 			cursor = conn.cursor()
# 			cursor.callproc('sp_validateLogin',(_username,))
# 			data = cursor.fetchall()

# 			if len(data) > 0:
# 				session['username'] = _username
# 				session['user_id'] = data[0][0]
# 				cursor.close()
# 				conn.close()
# 				return redirect('/showUserPage')

# 			elif len(data) is 0:
# 				cursor.callproc('sp_createUser',(_username,))
# 				conn.commit()
# 				cursor.callproc('sp_validateLogin',(_username,))
# 				data = cursor.fetchall()
# 				session['username'] = _username
# 				session['user_id'] = data[0][0]
# 				cursor.close()
# 				conn.close()
# 				return redirect('/showUserPage')

# 			else:
# 				return json.dumps({'error':str(data[0])})
# 		else:
# 			return json.dumps({'html':'<span>Enter the required fields</span>'})
# 	except Exception as e:
# 		return json.dumps({'error':str(e)})
# 	else:
# 		cursor.close()
# 		conn.close()


if __name__ == "__main__":
	app.run(host = '127.0.0.1', port = 5000)


