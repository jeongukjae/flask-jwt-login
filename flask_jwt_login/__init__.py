# -*- coding:utf8 -*-

from flask import current_app, request, redirect, abort
from functools import wraps

import jwt

__version__ = '0.0.1'

# default config for this module
DEFAULT_CONFIG = {
	"HASH_ALGORITHM" : "HS512"
}

JWT_COOKIE_NAME = 'token'

class JWT:
	def __init__(self, app=None):
		self.auth_handler = None
		self.unauthorized = None
		if app is not None:
			self.init_app(app)

	def init_app(self, app, config={}):
		# set default config
		for k, v in DEFAULT_CONFIG.items():
			app.config.setdefault(k, v)
		app.config.setdefault("JWT_SECRET_KEY", app.config["SECRET_KEY"])

		# set user's config
		for k, v in config.items():
			app.config.setdefault(k, v)

		app.extensions['jwt'] = self

	def authentication_handler(self, callback):
		self.auth_handler = callback
		return callback

	def unauthorized_handler(self, callback):
		self.unauthorized = callback
		return callback

def process_login(id, pw):
	user = current_app.extensions['jwt'].auth_handler(id, pw)
	if user is None:
		return None

	token = jwt.encode(user.__dict__, \
		current_app.config["JWT_SECRET_KEY"], \
		algorithm=current_app.config["HASH_ALGORITHM"])
	return token

def get_current_user(request):
	token = request.cookies.get(JWT_COOKIE_NAME)
	if token is not None:
		try:
			jwt_token = jwt.decode(token, \
				current_app.config["JWT_SECRET_KEY"], \
				algorithm=[current_app.config['HASH_ALGORITHM']])
		except jwt.exceptions.DecodeError as e:
			# Signature verification failed
			jwt_token = None

		return jwt_token

	return None

# login required decorator
def login_required(func):

	@wraps(func)
	def decorator(*args, **kwargs):
		jwt_login = current_app.extensions['jwt']
		
		token = request.cookies.get(JWT_COOKIE_NAME)

		# token does not exist
		if token is None:
			if jwt_login.unauthorized is None:
				return abort(400)
			return jwt_login.unauthorized()

		try:
			jwt_token = jwt.decode(token, \
				current_app.config["JWT_SECRET_KEY"], \
				algorithm=[current_app.config['HASH_ALGORITHM']])
		except jwt.exceptions.DecodeError:
			if jwt_login.unauthorized is None:
				return abort(400)
			return jwt_login.unauthorized()
		# identity_handler does not exist
		return func(*args, **kwargs)

	return decorator