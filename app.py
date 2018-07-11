import requests
import sys
import os 
import json
from flask import Flask, request, render_template, redirect, url_for, Blueprint, jsonify
from fbmq import Page, Template, Template, QuickReply
from config import *

from flask_material import Material  
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required

page = Page(FACEBOOK_TOKEN)
app = Flask(__name__)
errors = Blueprint('errors', __name__)
data = None

app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY

Material(app)
app.config.setdefault('MATERIAL_SERVE_LOCAL', True)

# straight from the wtforms docs:
class TelephoneForm(Form):
	country_code = IntegerField('Country Code', [validators.required()])
	area_code = IntegerField('Area Code/Exchange', [validators.required()])
	number = TextField('Number')

class ExampleForm(Form):
	field1 = TextField('First Field', description='This is field one.')
	field2 = TextField('Second Field', description='This is field two.',
					   validators=[Required()])
	hidden_field = HiddenField('You cannot see this', description='Nope')
	recaptcha = RecaptchaField('A sample recaptcha field')
	radio_field = RadioField('This is a radio field', choices=[
		('head_radio', 'Head radio'),
		('radio_76fm', "Radio '76 FM"),
		('lips_106', 'Lips 106'),
		('wctr', 'WCTR'),
	])
	checkbox_field = BooleanField('This is a checkbox',
								  description='Checkboxes can be tricky.')

	# subforms
	mobile_phone = FormField(TelephoneForm)

	# you can change the label as well
	office_phone = FormField(TelephoneForm, label='Your office phone')

	ff = FileField('Sample upload')

	submit_button = SubmitField('Submit Form')


	def validate_hidden_field(self, form, field):
		raise ValidationError('Always wrong')

@app.route('/form')
def test_form():
	form = ExampleForm()   
	return render_template('test.html', form = form) 

@app.route('/')
def index():
	return redirect(url_for('payment'))

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
	print data
	page.handle_webhook(request.get_data(as_text=True))
	return "ok"

@page.handle_message
def handle_message(event):
	pass

@page.after_send
def after_send(payload, response):
	print response

@errors.app_errorhandler(Exception)
def handle_error(error):
	message = [str(x) for x in error.args]
	status_code = error.status_code
	success = False
	response = {
		'success': success,
		'error': {
			'type': error.__class__.__name__,
			'message': message
		}
	}
	return jsonify(response), status_code

@app.errorhandler(404)
def page_not_found(e):
	return jsonify({'error':'not found'}), 404

url_messenger_profile = 'https://graph.facebook.com/v2.6/me/messenger_profile'
url_messenger_message = 'https://graph.facebook.com/v2.6/me/messages'
token = FACEBOOK_TOKEN
casa = CASA_LINK

params = {
	"access_token": token
}
headers = {
	"Content-Type": "application/json"
}

page.greeting('Hello {{user_full_name}} Welcome to FB Messenger Chatbot')


page.show_starting_button("START_PAYLOAD")

@page.callback(['START_PAYLOAD'])
def start_payload_callback(payload, event):
	sender_id = event.sender_id
	page.typing_on(sender_id)
	page.send(sender_id, u"Welcome! Nice to see you here. I'm KREDIT Chatbot and I will help you response quickly as an option menu below.")
	page.send(sender_id, u"Welcome to KREDIT MFI Plc. With this chatbot you can do whatever you want.")
	page.send(sender_id, u"And we are really happy to see your feedback. Thanks! :)")
	page.typing_off(sender_id)
	print ("Let's start! %s", sender_id)

persistent_menu_data = json.dumps(
{
  "persistent_menu":[
	{
	  "locale":"default",
	  "composer_input_disabled": False,
	  "call_to_actions":[
			{
				"title":"My Account",
				"type":"nested",
				"call_to_actions":[
					{
						"title":"Login",
						"type":"account_link",    
						"url":"https://ebotmessenger.herokuapp.com/payment"
					},
					{
						"title":"Top Up",
						"type":"postback",    
						"payload":"TOPUP_PAYLOAD"
					},
					{
						"title":"ATM Location",
						"type":"postback",
						"payload":"ATM_PAYLOAD"
					}
				]
			},
			{
				"title":"My Profile",
				"type":"nested",
				"call_to_actions":[
					{
						"title":"Take Photo AR",
						"type":"postback",    
						"payload":"CHECK_BALANCE_PAYLOAD"
					},
					{	
						"title":"Menu2",
						"type":"postback",    
						"payload":"PAYBILL_PAYLOAD"
					},
					{
						"title":"Menu3",
						"type":"postback",    
						"payload":"PAYBILL_PAYLOAD"
					}
				]
			},
			{
				"type":"web_url",
				"title":"Help",
				"url":"http://www.messenger.com/",
				"webview_height_ratio":"full"
			}
	  ]
	}
  ]
})
requests.post(url=url_messenger_profile, params=params, headers=headers, data=persistent_menu_data)

@page.callback(['CHECK_BALANCE_PAYLOAD'])
def click_check_balance_payload(payload, event):
	page.send(event.sender_id, 'click check balance')

@page.callback(['ATM_PAYLOAD'])
def click_atm_payload(payload, event):
	print 'location access'
	print "id ", event.sender_id
	location_request = json.dumps({
		"recipient":{
			"id": event.sender_id
		},
		"message":{
			"text": "Please send me your current location now. I will help find the nearest ATM for you.",
			"quick_replies":[{
				"content_type":"location"
			}]	
		}
	})
	print "json: %s", location_request
	requests.post(url=url_messenger_message, params=params, headers=headers, data=location_request)
	print "data: ",data

@page.callback(['TOP_UP_PAYLOAD'])
def click_top_up_payload(payload, event):
	page.send(event.sender_id, 'click top up')

@page.callback(['PAYBILL_PAYLOAD'])
def click_persistent_menu_find_pitch(payload, event):
	sender_id = event.sender_id
	page.typing_on(sender_id)
	page.send(sender_id, "you clicked %s menu" % payload)
	

	quick_replies = [
		QuickReply(title="Action", payload="PICK_ACTION"),
		QuickReply(title="Comedy", payload="PICK_COMEDY")
	]

	page.send(sender_id, 
		  "What's your favorite movie genre?",
		  quick_replies=quick_replies,
		  metadata="DEVELOPER_DEFINED_METADATA")
	page.typing_off(sender_id)
	print("you clicked %s menu" % payload)

@page.callback(['NEWS'])
def click_persistent_menu_reminder(payload, event):
	sender_id = event.sender_id
	page.send(sender_id, "you clicked %s menu" % payload)
	print("you clicked %s menu" % payload)

@page.callback(['CONTACT_INFO_PAYLOAD'])
def click_persistent_menu_help(payload, event):
	sender_id = event.sender_id
	page.send(sender_id, "you clicked %s menu" % payload)
	print("you clicked %s menu" % payload)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run('0.0.0.0', port)
