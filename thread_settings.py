from fbmq import Template, QuickReply
from app import page, ProductConfig
import sys
import requests
import json

url_messenger_profile = 'https://graph.facebook.com/v2.6/me/messenger_profile'
token = ProductConfig.FACEBOOK_TOKEN

params = {
	"access_token": token
}
headers = {
	"Content-Type": "application/json;charset=UTF-8"
}

# Greeting text
greeting_text_data = '''
{
	"greeting":[
	{
	  "locale":"default",
	  "text":"សួស្តី {{user_full_name}}"
	}
  ] 
}
'''
requests.post(url=url_messenger_profile, params=params, headers=headers, data=greeting_text_data)



page.show_starting_button("START_PAYLOAD")

@page.callback(['START_PAYLOAD'])
def start_payload_callback(payload, event):
	sender_id = event.sender_id
	page.typing_on(sender_id)
	page.send(sender_id, "Welcome to EBot Messenger. What can I help you?")
	page.typing_off(sender_id)
	print ("Let's start! %s", sender_id)

persistent_menu_data = '''{
  "persistent_menu":[
	{
	  "locale":"default",
	  "composer_input_disabled": false,
	  "call_to_actions":[
		{
		  "title":"My Account",
		  "type":"nested",
		  "call_to_actions":[
			{
			  "title":"Check Balance /ពិនិត្យទឹកប្រាក់",
			  "type":"postback",    
			  "payload":"PAYBILL_PAYLOAD"
			},
			{
			  "title":"Pay Bill",
			  "type":"postback",    
			  "payload":"PAYBILL_PAYLOAD"
			},
			{
			  "title":"Pay Bill",
			  "type":"postback",    
			  "payload":"PAYBILL_PAYLOAD"
			},
			{
			  "title":"History",
			  "type":"postback",
			  "payload":"HISTORY_PAYLOAD"
			},
			{
			  "title":"Contact Info",
			  "type":"postback",
			  "payload":"CONTACT_INFO_PAYLOAD"
			}
		  ]
		},
		{
		  "type":"web_url",
		  "title":"Latest News",
		  "url":"http://www.messenger.com/",
		  "webview_height_ratio":"full"
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
}'''
requests.post(url=url_messenger_profile, params=params, headers=headers, data=persistent_menu_data)





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

