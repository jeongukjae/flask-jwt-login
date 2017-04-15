# -*- coding:utf8 -*-
from flask import current_app, request, redirect, abort
from functools import wraps

# use jwt module
import jwt

# module version
__version__ = '0.0.1'

# default config for this module
DEFAULT_CONFIG = {
	"HASH_ALGORITHM" : "HS512"
}

# JWT COOKIE NAME
# If you want to use an another cookie name, edit this constant.
JWT_COOKIE_NAME = 'token'

class JWT:
	# auth_handler: authentification handler
	# unauthorized: unauthorized handler
	def __init__(self, app=None):
		self.auth_handler = None
		self.unauthorized = None
		if app is not None:
			self.init_app(app)

	# Use secret key of flask app
	def init_app(self, app, config={}):
		# set default config
		for k, v in DEFAULT_CONFIG.items():
			app.config.setdefault(k, v)
		app.config.setdefault("JWT_SECRET_KEY", app.config["SECRET_KEY"])

		# set user's config
		for k, v in config.items():
			app.config.setdefault(k, v)

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

# get token with id and password
# return jwt token
# pass id and password parameters to authentification handler(auth_handler)
def process_login(id, pw):
	user = current_app.extensions['jwt'].auth_handler(id, pw)
	if user is None:
		return None

	token = jwt.encode(user.__dict__, \
		current_app.config["JWT_SECRET_KEY"], \
		algorithm=current_app.config["HASH_ALGORITHM"])
	return token

# get user info from request
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
