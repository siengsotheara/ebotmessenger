from flask import render_template, request, url_for, session, Flask, escape, redirect, Response
from functools import wraps
from app import app , jsonify
from core.logics.user import UserLogic, users

def check_auth(username, password):
	user = users.authenticate(username, password)
	if user:
		session['username'] = user.username
	return user

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if 'username' not in session:
			auth = request.authorization
			if not auth or not check_auth(auth.username, auth.password):
				if 'X-Requested-With' in request.args and request.args['X-Requested-With']=='XMLHttpRequest':
					return authenticate()
				else:
					return redirect(url_for('admin.SecurityView:login', next=request.url))
		return f(*args, **kwargs)
	return decorated