# -*- coding:utf8 -*-
from flask import current_app, request

# use jwt module
import jwt

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
def get_current_user(token=None):
	if token is None:
		token = request.cookies.get(current_app.config["JWT_COOKIE_NAME"])

	if token is not None:
		try:
			jwt_token = jwt.decode(token, \
				current_app.config["JWT_SECRET_KEY"], \
				algorithms=[current_app.config['HASH_ALGORITHM']])
		except jwt.exceptions.DecodeError as e:
			# Signature verification failed
			jwt_token = None

		return jwt_token

	return None
