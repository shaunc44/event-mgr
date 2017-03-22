from flask import Flask, render_template, session, g, json, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import datetime
import os
# from werkzeug import generate_password_hash, check_password_hash #Do I need this anymore?


mysql = MySQL()
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = open('secret_key', 'rb').read() 


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


@app.route('/addUserEvent', methods=['POST', 'GET'])
def addUserEvent():
	try:
		if session.get('user_id'):
			_user_id = session.get('user_id')
			_title = request.form['inputTitle']
			# conn = mysql.connect()
			# cursor = conn.cursor()
			# cursor.callproc('sp_getTitle',(_title, _description, _location))
			# cursor.callproc('sp_addEvent',(_title, _description, _location))
			# data = cursor.fetchall()
			# print (data)

			# _title = data[0][0]
			print ("UserID: ", _user_id)
			print ("Title: ", _title)

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_getEventId',(_title,)) #not returning event_id b/c title isn't correct
			data = cursor.fetchall()
			print ("getEventId Data: ", data)
			_event_id = _event[0][0]
			# print ("Event: ", _event)
			# print ("EventID: ", _event_id)
			# cursor.close()
			# conn.close()

			cursor.callproc('sp_addUserEvent',(_user_id, event_id))
			conn.commit()
			data = cursor.fetchall()
			print ("AddUserEvent Data: ", data)

			cursor.close()
			conn.close()

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
			_title = request.form['inputTitle']
			_description = request.form['inputDescription']
			_location = request.form['inputLocation']

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_addEvent',(_title, _description, _location))
			# conn.commit()
			data = cursor.fetchall()
			# session['title'] = data[0][0]
			# print ("Title: ", data[0][0])
			# print ("AddEvent Data: ", data)a;dlkjfads;

			if len(data):
				conn.commit()
				cursor.close()
				conn.close()
				addUserEvent()
				# return redirect('/addUserEvent')
				# return redirect('/showUserPage')
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
			print ("SignUp Data: ", data)

			if len(data) > 0:
				if data[0][2] == _password:
					session['user_id'] = data[0][0]
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



if __name__ == "__main__":
	app.run(host = '127.0.0.1', port = 5000)


