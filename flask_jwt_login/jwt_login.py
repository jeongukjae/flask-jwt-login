# -*- coding: utf8 -*-
from flask import current_app, abort, request
from functools import wraps

from .config import DEFAULT_CONFIG 

import jwt

class JWT:
	# auth_handler: authentification handler
	# unauthorized: unauthorized handler
	def __init__(self, app=None):
		self.auth_handler = None
		self.unauthorized = None
		
		if app is not None:
			self.init_app(app)

	# Use secret key of flask app
	def init_app(self, app):
		# set default config
		for k, v in DEFAULT_CONFIG.items():
			app.config.setdefault(k, v)

		app.config.setdefault("JWT_SECRET_KEY", app.config["SECRET_KEY"])

		# register this class to flask extension
		app.extensions['jwt'] = self

	# register authenfication handler
	def authentication_handler(self, callback):
		self.auth_handler = callback
		return callback

	# register unauthorized handler
	def unauthorized_handler(self, callback):
		self.unauthorized = callback
		return callback

# login required decorator
def login_required(func):

	@wraps(func)
	def decorator(*args, **kwargs):
		jwt_login = current_app.extensions['jwt']
		
		token = request.cookies.get(current_app.config["JWT_COOKIE_NAME"])

		# token does not exist
		if token is None:
			if jwt_login.unauthorized is None:
				abort(501)
			return jwt_login.unauthorized()

		try:
			jwt_token = jwt.decode(token, \
				current_app.config["JWT_SECRET_KEY"], \
				algorithms=[current_app.config['HASH_ALGORITHM']])
		except jwt.exceptions.DecodeError:
			if jwt_login.unauthorized is None:
				abort(501)
			return jwt_login.unauthorized()

		return func(*args, **kwargs)

	return decorator
