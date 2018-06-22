from fbmq import Template, QuickReply
from app import page, ProductConfig, url_for, render_template, redirect
import sys
import requests
import json

url_messenger_profile = 'https://graph.facebook.com/v2.6/me/messenger_profile'
token = ProductConfig.FACEBOOK_TOKEN

params = {
	"access_token": token
}
headers = {
	"Content-Type": "application/json"
}

# Greeting text
greeting_text_data = json.dumps({
	"greeting" : [
	{
	  "locale":"default",
	  "text":u"Hello {{user_full_name}} ាសដាសដសដ"
	}
 ]})
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
			  "title":"Check Balance",
			  "type":"postback",    
			  "payload":"CHECK_BALANCE_PAYLOAD"
			},
			{
			  "title":"Transfer Money",
			  "type":"postback",    
			  "payload":"PAYBILL_PAYLOAD"
			},
			{
			  "title":"Top up",
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
		  "url":"https://kredit.com.kh/en",
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

@page.callback(['CHECK_BALANCE_PAYLOAD'])
def click_check_balance_payload(payload, event):
	page.send(event.sender_id, 'click check balance')


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

