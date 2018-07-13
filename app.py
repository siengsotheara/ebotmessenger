import requests
import sys
import os 
import json
import urlparse
import uuid
from werkzeug.exceptions import HTTPException
from flask import Flask, request, render_template, redirect, url_for, Blueprint, jsonify
from fbmq import Page, Template, Template, QuickReply
from config import FACEBOOK_TOKEN,VERIFY_TOKEN, SECRET_KEY,CASA_LINK	

from flask_wtf import FlaskForm
from wtforms import TextField, HiddenField, ValidationError, RadioField,BooleanField, SubmitField, IntegerField, FormField, PasswordField, validators
from wtforms.validators import Required

page = Page(FACEBOOK_TOKEN)
app = Flask(__name__)
errors = Blueprint('errors', __name__)
data = None

app.config['SECRET_KEY'] = SECRET_KEY

class LoginForm(FlaskForm):
	username = TextField("Username", render_kw = {
			'placeholder': 'Enter your username',
			'data-val':'true',
			'data-val-required':'Input Required'
		})
	password = PasswordField("Password", render_kw= {
			'placeholder':'Enter your password',
			'data-val':'true',
			'data-val-required':'Input Required'})

	redirect_uri = HiddenField()
	account_linking_token = HiddenField()

	submit_button = SubmitField("Login")

@app.route('/login/authorize', methods=['GET', 'POST'])
def login():
	"""
	Account Linking Token is never used in this demo, however it is
	useful to know about this token in the context of account linking.
	It can be used in a query to the Graph API to get Facebook details
	for a user. Read More at:
	https://developers.facebook.com/docs/messenger-platform/account-linking	
	"""

	redirect_uri = request.args.get('redirect_uri')
	account_linking_token = request.args.get('account_linking_token')
	print account_linking_token
	form = LoginForm()
	
	if request.method == 'POST':
		if form.validate_on_submit():
			username = form.username.data
			password = form.password.data
			redirectURI = form.redirect_uri
			
			if username == "admin" and password == "admin":
				return redirect(url_for('/{0}&authorization_code={1}'.format(redirectURI, uuid.uuid1().hex)))

	return render_template('login.html', form = form , redirect_uri=redirect_uri)

@app.route('/payment')
def payment():
	return render_template('payment.html')


@app.route('/webhook', methods=['GET'])
def validate():
	if request.args.get('hub.mode', '') == 'subscribe' and \
					request.args.get('hub.verify_token', '') == VERIFY_TOKEN:

		print("Validating webhook")

		return request.args.get('hub.challenge', '')
	else:
		return 'Failed validation. Make sure the validation tokens match.'

@app.route('/webhook', methods=['POST'])
def webhook():
	data = request.get_json()
	print "data: ",data
	page.handle_webhook(request.get_data(as_text=True))
	return "ok", 200

@page.handle_message
def handle_message(event):
	pass

@page.after_send
def after_send(payload, response):
	print "response:", response

@app.errorhandler(Exception)
def all_exception_handler(error):
	message = [str(x) for x in error.args]

	# if isinstance(error, HTTPException):
	# 	code = error.code

	response = {
		'error': {
			'type': error.__class__.__name__,
			'message': message
		}
	}   
	return jsonify(response)

@errors.app_errorhandler(Exception)
def handle_error(error):
	message = [str(x) for x in error.args]
	status_code = error.status_code
	response = {
		'error': {
			'type': error.__class__.__name__,
			'message': message
		}
	}

	return jsonify(response), status_code

import fb.threading_setup

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run('0.0.0.0', port)
