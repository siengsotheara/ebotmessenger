from fbmq import Template, QuickReply
from app import page, ProductConfig, url_for, render_template, redirect, request
import sys
import requests
import json

url_messenger_profile = 'https://graph.facebook.com/v2.6/me/messenger_profile'
token = ProductConfig.FACEBOOK_TOKEN
casa = ProductConfig.CASA_LINK

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
	  "text": u"សួស្តី {{user_full_name}} សូមស្វាគមន៍មកកាន់ ក្រេឌីត FB Messenger Chatbot សូមចុច Get Start ដើម្បីចាប់ផ្តើមជាមួយគ្នា។"
	}
 ]})
requests.post(url=url_messenger_profile, params=params, headers=headers, data=greeting_text_data)



page.show_starting_button("START_PAYLOAD")

@page.callback(['START_PAYLOAD'])
def start_payload_callback(payload, event):
	sender_id = event.sender_id
	page.typing_on(sender_id)
	page.send(sender_id, u"{{user_full_name}}, welcome! Nice to see you here. I'm KREDIT Chatbot and I will help you response quickly as an option menu below.")
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
						"title":"Check Balance",
						"type":"web_url",    
						"url":"https://ebotmessenger.herokuapp.com/payment",
						"webview_height_ratio":"full"
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
				"title":"My Profile",
				"type":"nested",
				"call_to_actions":[
					{
						"title":"Menu1",
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
					},
					{
						"title":"Menu4",
						"type":"postback",
						"payload":"HISTORY_PAYLOAD"
					},
					{
						"title":"Menu5",
						"type":"postback",
						"payload":"CONTACT_INFO_PAYLOAD"
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
	pass


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

