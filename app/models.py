from . import db
from time import time
from datetime import date
from flask import json, jsonify
class Users(db.Model):
	person_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
	gender = db.Column(db.String(10))
	age = db.Column(db.Integer)
	profile_photo = db.Column(db.String(80))
	date_created = db.Column(db.String(30))
	bio = db.Column(db.String(250))

	def _init_(self, first_name, last_name, username, password, age, gender, profile_photo, bio):
		self.person_id = int(Users.returnID())
		self.first_name = first_name
		self.last_name  = last_name
		self.username = username
		self.password = password
		self.age = age
		self.gender = gender
		self.profile_photo = profile_photo
		self.date_created = Users.timeinfo()
		self.bio = bio
	
	@staticmethod
	def returnID():
		new_id = long(time())
		return new_id
	
	@staticmethod
	def timeinfo():
		"""Forats the date and time"""
		d = date.today();
		return "{0:%A}, {0:%B} {0:%d}, {0:%y}".format(d)
	
	def _repr_(self):
		return '<User %r>' % (self.username)

	def get_image_url(self):
		return '/uploads/{0}'.format(self.image)
	
	def toJSON(self):
		return jsonify(username = self.username, userid = self.id)