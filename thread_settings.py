from fbmq import Template, QuickReply
from app import page, ProductConfig
import sys
import requests
import json


thread_settings_url = 'https://graph.facebook.com/v2.6/me/messenger_profile'
token = ProductConfig.FACEBOOK_TOKEN

params = {
	"access_token": token
}
headers = {
	"Content-Type": "application/json"
}

# Greeting text
greeting_text_data = '''
{
	"greeting":[
	{
	  "locale":"default",
	  "text":"Hi {{user_full_name}} Welcome to Phillip Banki Plc. Bot. May I help you?"
	}
  ] 
}
'''
print ("greeting_text_data: " + greeting_text_data)
requests.post(thread_settings_url, params=params, headers=headers, data=greeting_text_data)

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
	  "composer_input_disabled": true,
	  "call_to_actions":[
		{
		  "title":"My Account",
		  "type":"nested",
		  "call_to_actions":[
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
	},
	{
	  "locale":"default",
	  "composer_input_disabled":false,
	  "call_to_actions":[
		{
		  "title":"Pay Bill",
		  "type":"postback",
		  "payload":"PAYBILL_PAYLOAD"
		}
	  ]    
	}
  ]
}'''
requests.post(url=thread_settings_url, params=params, headers=headers, data=persistent_menu_data)

quick_replies = [
	QuickReply(title="Action", payload="PICK_ACTION"),
	QuickReply(title="Comedy", payload="PICK_COMEDY")
]


page.send(recipient_id, 
		  "What's your favorite movie genre?",
		  quick_replies=quick_replies,
		  metadata="DEVELOPER_DEFINED_METADATA")


page.send(recipient_id, Template.Generic([
  Template.GenericElement("rift",
						  subtitle="Next-generation virtual reality",
						  item_url="https://www.oculus.com/en-us/rift/",
						  image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
						  buttons=[
							  Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
							  Template.ButtonPostBack("tigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
							  Template.ButtonPhoneNumber("Call Phone Number", "+855010335644")
						  ]),
  Template.GenericElement("touch",
						  subtitle="Your Hands, Now in VR",
						  item_url="https://www.oculus.com/en-us/touch/",
						  image_url=CONFIG['SERVER_URL'] + "/assets/touch.png",
						  buttons=[
							  Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
							  Template.ButtonPostBack("tigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
							  Template.ButtonPhoneNumber("Call Phone Number", "+855010335644")
						  ])
]))

@page.callback(['PAYBILL_PAYLOAD'])
def click_persistent_menu_find_pitch(payload, event):
	sender_id = event.sender_id
	page.typing_on(sender_id)
	page.send(sender_id, "you clicked %s menu" % payload)
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

