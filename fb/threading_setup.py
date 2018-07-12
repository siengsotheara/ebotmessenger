from app import FACEBOOK_TOKEN, CASA_LINK
from app import json, page, requests

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
	d = json.dumps({
		"recipient":{
			"id":sender_id
		},
		"message":{
			"attachment":{
			"type":"template",
			"payload":{
				"template_type":"button",
				"text":"Try the log in button!",
				"buttons":[{
					"type": "account_link",
					"url": "https://ebotmessenger.herokuapp.com/login/authorize"
					}]
				}
			}
		}
	})
	requests.post(url=url_messenger_message, params=params, headers=headers, data=d)
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
				"title":"Help",
				"type":"postback",
				"payload":"Payload"
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
