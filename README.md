# Flask-JWT-Login

[![Build Status](https://travis-ci.org/JeongUkJae/Flask-JWT-Login.svg?branch=master)](https://travis-ci.org/JeongUkJae/Flask-JWT-Login) [![Coverage Status](https://coveralls.io/repos/github/JeongUkJae/Flask-JWT-Login/badge.svg?branch=master)](https://coveralls.io/github/JeongUkJae/Flask-JWT-Login?branch=master) [![PyPI](https://img.shields.io/pypi/v/Flask-JWT-Login.svg)]()

Flask extension that helps authentication using JWT(Json Web Token)

## Guide

### How to initiate

```Python
from flask import Flask
from flask_jwt_login import JWT

app = Flask(__name__)	# create app object
jwt = JWT(app)			# initialize flask_jwt_login
```

### Configuration

**app.py**

```Python
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')
```

**config.py**

```Python
class Config(object):
    SECRET_KEY = 'random secret key for development'
    HASH_ALGORITHM = 'HS512' 
    # hash algorithm to use at encode and decode token
    JWT_COOKIE_NAME = 'token'
    # token name to be used
    
    # if you don't specify HASH_ALGORITHM or JWT_COOKIE_NAME,
    # they will have default value. (HS512 and token)
```

**Which hash algorithm do I have to use?**

Refer [this link (PyJWT Documentation - Digital Signature Algorithms)](http://pyjwt.readthedocs.io/en/latest/algorithms.html)

### authentication

**authentication handler**

```Python
...
...

# initialize
jwt = JWT(app)

# user data class
# I want to recommend you to add hashed passsword data into token
class User():
	def __init__(self, id, pw, name):
		self.id = id
		self.pw = pw
		self.name = name

	def __repr__(self):
		return "User(id=%s, password=%s, name=%s)" % (self.id, self.pw, self.name)
		
# You have to write a function that check users' ids and passwords.
@jwt.authentication_handler
def authentication_handler(id, pw):
	for row in user_table:
		if row['id'] == id and row['pw'] == pw:
			return User(row['id'], row['pw'], row['name'])

	# if there is no matching user, returns None
	return None
```

**process login**

```Python
from flask_jwt_login import process_login

@app.route('/some_url')
def some_function():
	token = process_login(request.form["id"], request.form["pw"])
	# this token will be the value returned from authentication handler
	
	response = make_response("sign in")
	response.set_cookie(TOKEN_NAME, token)
	return response
```

**unauthorized handler**

```Python
@jwt.unauthorized_handler
def unauthorized_handler():
	# if authentication failed, this handler will be performed
	return 'Unauthorized Access', 501
```

### Protected Page & User Information

**login required & get current user**

```Python
# this url is only accessed by users who have a valid token.
@app.route("/protected")
@login_required
def protected():
	return "Protected Page. name :" + get_current_user()["name"]
```