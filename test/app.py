# -*- coding : utf8 -*-
from flask import Flask, redirect, request, make_response
from flask_jwt_login import JWT, login_required, JWT_COOKIE_NAME, get_current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "super secret"
jwt = JWT(app)

class User(object):
	def __init__(self, id):
		self.id = id

	def __str__(self):
		return "User(id=%s)" % (self.id)

user_table = {"idtest1":"pwtest1"} 

@jwt.authentication_handler
def authentication_handler(id, pw):
	if id in user_table and user_table[id] == pw:
		return User(id)
	return None

@app.route("/")
def main():
	return redirect("login")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return "<form method='post'>" +\
					"<input type='text' name='id'>" +\
					"<input type='password' name='pw'>" +\
					"<input type='submit'>" +\
				"</form>"

	token = jwt.process_login(request.form["id"], request.form["pw"])
	print(token)
	if token is not None:
		response = make_response("<a href='/protected'>GO!<a>")
		response.set_cookie(JWT_COOKIE_NAME, token)
		return response
	return "Error!"

@app.route("/protected")
@login_required
def protected():
	return "Protected Page. token :" + get_current_user(request)["id"]

if __name__ == "__main__":
	app.run(debug=True)