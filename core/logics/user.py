from core.logics.base import LogicBase
from core.models import User
from passlib.apps import custom_app_context as pwd_context

import base64
import requests
import json

def hash_password(password):
	return pwd_context.encrypt(password)

def verify_password(password1, password2):
	return pwd_context.verify(password1, password2)

class UserLogic(LogicBase):
	def __init__(self):
		self.__classname__ = User
		self.headers = {
			"Content-Type": "application/json"
		}

	def authenticate_local(self, username, password):
		user = self._active().filter(User.username==username.lower()).first()
		if user:
			verify = verify_password(username.lower()  + str(password), user.password)
			if not verify:
				return None
		return user

	def authenticate_webportal(self, username, password):
		"""
		Login Webportal ESB

		example: 

		requests.post(url='http://192.168.100.13:8080/esb/oauth/token', headers={'Content-Type':'application/json'}, data={})
		"""

		user = User()
	
		request_token = json.dumps({
			'app_id':'BANKINGBOT',
			'client_id':'bankingbot_web',
			'client_secret':'KV08pFPMVN/QZCi8BwJCGmzVy6gPFZuQjuTSbK6jeBM=',
			'grant_type':'password',
			'username': username,
			'password': base64.b64encode(password),
			'scope':'read,write'
		})

		webportal_data = requests.post(url='http://192.168.100.13:8080/esb/oauth/token', headers=self.headers, data=request_token)
			
		if webportal_data.status_code == requests.codes.ok:
			login_request = requests.get(url='http://192.168.100.13:8080/esb/oauth/get/token', headers={"Authorization" : webportal_data.json()['access_token']})
			if login_request.status_code != requests.codes.ok:
				return None
			else:
				user.username = username
				user.password = hash_password(user.username + password)
		else:
			return None

		return user

	def _insert(self, obj):
		obj.username = obj.username.lower()
		obj.password = hash_password(obj.username + obj.password)
		LogicBase._insert(obj)

	#def add_user_webportal(self, obj):
	#	data = json.dumps({
	#		"app_id": "BANKINGBOT",
	#		"username": obj.username,
	#		"password": base64.b64encode(obj.password)
	#	})

	#	response = requests.post(url='http://192.168.100.13:8080/esb/oauth/user', headers=self.headers, data=data)
	#	if response.status_code == requests.codes.bad_request:


	def change_password(self, obj):
		obj.password = hash_password(obj.username + obj.password)
		LogicBase._update(obj)

users = UserLogic()