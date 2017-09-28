# -*- coding : utf8 -*-
from flask import Flask, redirect, request, make_response
from flask_jwt_login import JWT, login_required, get_current_user, process_login

# add token name
TOKEN_NAME = 'token'

# create flask app and add configs
app = Flask(__name__)
app.config["SECRET_KEY"] = "super secret"
app.config["JWT_COOKIE_NAME"] = TOKEN_NAME

# make jwt object
jwt = JWT(app)

# make user data
class User():
	def __init__(self, id, pw, name):
		self.id = id
		self.pw = pw
		self.name = name

	def __repr__(self):
		return "User(id=%s, password=%s, name=%s)" % (self.id, self.pw, self.name)

# user data
user_table = [
	{'id' : 'idtest1', 'pw' : 'pwtest1', 'name' : 'nametest1'}
]

@jwt.authentication_handler
def authentication_handler(id, pw):
	for row in user_table:
		if row['id'] == id and row['pw'] == pw:
			return User(row['id'], row['pw'], row['name'])

	# if there is no matching user, returns None
	return None

@app.route("/")
def main():
	return redirect("login")

@app.route("/login", methods=["GET", "POST"])
def login():
	# if method is 'GET', response is form
	if request.method == "GET":
		return "<form method='post'>" +\
					"<input type='text' name='id'>" +\
					"<input type='password' name='pw'>" +\
					"<input type='submit'>" +\
				"</form>"

	# if method is 'POST'
	# create token
	token = process_login(request.form["id"], request.form["pw"])

	# if token exists, user can sign in.
	if token is not None:
		# make response to add cookie
		response = make_response("<a href='/protected'>GO!<a>")
		response.set_cookie(TOKEN_NAME, token)
		return response

	# if token is None, there is no matching user.
	return "Error!"

# this url is only accessed by users who have a valid token.
@app.route("/protected")
@login_required
def protected():
	return "Protected Page. name :" + get_current_user()["name"]

if __name__ == "__main__":
	app.run(debug=True)