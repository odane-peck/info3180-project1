import os
from datetime import date
from forms import CreateUserForm, ProfileInfo
from app import app, models, forms, db
from models import Users 
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, send_from_directory, session,make_response
from sqlalchemy.sql import exists
from werkzeug.wsgi import SharedDataMiddleware
#import alg#

#@app.route(/matched profiles?)
# def Matchprofile():
	# pass current user profile to algorithm
	
	#matched_users = [('username1', 'photo.jpg', '98%'), ('username2', 'photo2.jpg', '52%'), ('username3', 'photo3.jpg', '96%')]
	#return render_template('template.html', users=matched_users)

# @app.route('/api/api/route/database')
# def view():
	
@app.route('/api/profile/get')
def profiler():
	form = ProfileInfo()
	return render_template('ProfileInfo.html', form = form)
@app.route('/')
def home():
	form = CreateUserForm()
	return render_template('home.html')

@app.route('/profile', methods=['POST', 'GET'])
@app.route('/profile/<username>', methods = ['GET'])
def profile(username = None):
	form = CreateUserForm()
	user = None
	if request.method == 'POST':
		username = form.username.data
		if not db.session.query(exists().where(Users.username == username)).scalar():
			gender_type = form.gender.data + '.png';
			user = Users(first_name = form.firstname.data, last_name = form.lastname.data, username = username, password = form.password.data, age = int(form.age.data), gender = form.gender.data, profile_photo = gender_type, bio = form.bio.data)
			filefolder = app.config["UPLOAD_FOLDER"]
			file = request.files['image']
			if file and validate_file(file.filename):
				filename = secure_filename(file.filename)
				filename = '{0}.{1}'.format(user.username,filename.split('.')[-1])
				file.save(os.path.join(filefolder, filename))
				user.profile_photo = filename
			db.session.add(user)
			db.session.commit()
			user = Users.query.all()
			form = ProfileInfo()
			return render_template('ProfileInfo.html', form = form)
		else:
			flash('Username already in use.', 'danger')
			return render_template('form.html', form = form)
	elif username:
		users = Users.query.all()
		for user in users:
			if user.username == username:
				return render_template('profile.html', user = user)
	return render_template('form.html', form = form)

def validate_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def display_profile():
	if 'username' in session:
		return redirect(url_for('profile'), username = session['username'])
	return redirect(url_for('home'))

@app.route("/profiles", methods = ['GET'] )
def profiles():
	users = Users.query.all()
	# match = []
	
	# for user in users:
	# 	matching statements with user as param
	# 	if match leve good: 
	# 		match.append(user)
	"""Render the website profile page"""
	return render_template("profiles.html", users = users)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

def timeinfo():
	date.today()
	return "Today's date is {0:%a}, {0:%d} {0:%b} {0:%y}".format(d)

@app.route('/api/all') 
def JSONcall():
	users 					= Users.query.all()
	ls 						= []
	jSON					= {}
	for user in users:
		jSON['username'] 	= user.username 
		jSON['userid'] 		= user.person_id
		ls 					= ls + [jSON]
		jSON 				= {}
	
	return jsonify({'users' : ls})

# @app.route('/match')
# def match():
	# mymatch=Match()
	
	#render_template('match.html, mymatch=mymatch')
	
@app.route('/api/<username>')
def userJSON(username = None):
	users = Users.query.all()
	if not username:
		return render_template('404.html'), 404
	for user in users:
		if user.username == username:
			gender = "Female"
			if user.gender == 1:
				gender = "Male"
			jSON = {
				"userid"			: user.person_id,
				"username"			: user.username,
				"image"				: user.profile_photo,
				"gender"			: gender,
				"age"				: user.age,
				"profile_created_on": user.date_created
			} 
			return jsonify(jSON)
	return "User Not Found"

			
			
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, { '/uploads':  app.config['UPLOAD_FOLDER'] })

if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0",port="8081")

