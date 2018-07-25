import requests
import sys
import os 
import json
import uuid

from werkzeug.exceptions import HTTPException
from flask import Flask, request, render_template, redirect, url_for, Blueprint, jsonify
from fbmq import Page, Template, Template, QuickReply, NotificationType
from config import FACEBOOK_TOKEN,VERIFY_TOKEN, SECRET_KEY,CASA_LINK	
from flask_babel import Babel, refresh

page = Page(FACEBOOK_TOKEN)
app = Flask(__name__)
errors = Blueprint('errors', __name__)
data = None

app.config['SECRET_KEY'] = SECRET_KEY

babel = Babel(app)
ctx = app.app_context()
ctx.push()

@babel.localeselector
def get_locale():
	if 'language' in request.cookies:
		return request.cookies.get('language')
	else:
		return 'km'

@babel.timezoneselector
def get_locale():
	return 'UTC'

@app.route('/language/<code>')
def language(code):
	session['language'] = code
	refresh()
	return redirect(url_for('/'))


@app.route('/login/authorize', methods=['GET'])
def getLogin():
	"""
	Account Linking Token is never used in this demo, however it is
	useful to know about this token in the context of account linking.
	It can be used in a query to the Graph API to get Facebook details
	for a user. Read More at:
	https://developers.facebook.com/docs/messenger-platform/account-linking	
	"""

	redirect_uri = request.args.get('redirect_uri')
	account_linking_token = request.args.get('account_linking_token')
	
	return render_template('login.html', error='', redirect_uri=redirect_uri, account_linking_token=account_linking_token)

@app.route('/login/authorize', methods=['POST'])
def postLogin():
	"""
	Account Linking Token is never used in this demo, however it is
	useful to know about this token in the context of account linking.
	It can be used in a query to the Graph API to get Facebook details
	for a user. Read More at:
	https://developers.facebook.com/docs/messenger-platform/account-linking	
	"""

	redirectURI = None
	linkToken = None
	error = None

	if request.method == 'POST':
		if request.form['submit'] == "btn_login":
			username = request.form.get('username')
			password = request.form.get('password')
			redirectURI = request.form.get('redirectURI')
			linkToken = request.form.get('linkToken')
			
			if username == "admin" and password == "admin":
				return redirect('{0}&authorization_code={1}'.format(redirectURI, uuid.uuid1().hex))
			else:
				error = "username or password incorrect!"
	return render_template('login.html', error=error, redirect_uri=redirectURI, account_linking_token=linkToken)
	

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
	print "response:", response.json()


#@app.errorhandler(Exception)
#def all_exception_handler(error):
#	message = [str(x) for x in error.args]

#	# if isinstance(error, HTTPException):
#	# 	code = error.code

#	response = {
#		'error': {
#			'type': error.__class__.__name__,
#			'message': message
#		}
#	}   
#	return jsonify(response)

#@errors.app_errorhandler(Exception)
#def handle_error(error):
#	message = [str(x) for x in error.args]
#	status_code = error.status_code
#	response = {
#		'error': {
#			'type': error.__class__.__name__,
#			'message': message
#		}
#	}

#	return jsonify(response), status_code

import threading_setup
import register_blueprint

@app.route('/')
def home():
	return redirect(url_for('admin.HomeView:index'))


ctx.pop()