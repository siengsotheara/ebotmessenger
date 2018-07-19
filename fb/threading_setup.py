from app import FACEBOOK_TOKEN, CASA_LINK
from app import json, app, page, requests, data, QuickReply, NotificationType, FacebookUtil, UserProfile

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
greeting_data = json.dumps({
	"greeting": [
			{
				"locale":"default",
				"text": "Hello {{user_full_name}} I'm PhillipBot. Thank for getting in touch with us on Messenger. Please send us any questions you may have"
			}
		]
})
requests.post(url=url_messenger_profile, params=params, headers=headers,data=greeting_data)


page.show_starting_button("START_PAYLOAD")

@page.callback(['START_PAYLOAD'])
def start_payload_callback(payload, event):
	sender_id = event.sender_id
	fbutil = FacebookUtil() 
	profile = UserProfile(fbutil._user_profile(event.sender_id, FACEBOOK_TOKEN))
	print profile.first_name
	print profile.last_name
	
	page.typing_on(sender_id)
	page.send(sender_id, profile.last_name + ", welcome! Nice to see you here :). I'm PhillipBot. You can ask me with quick reply pop up below and you can either choose option in right menu.")
	d = json.dumps({
		"recipient":{
			"id":sender_id
		},
		"message":{
			"attachment":{
			"type":"template",
			"payload":{
				"template_type":"button",
				"text":"Are you read to do this? You'll need to log in your customer's account so I can help you do more things.",
				"buttons":[
					{
						"type": "account_link",
						"url": "https://ebotmessenger.herokuapp.com/login/authorize"
					},
					{
						"title": "Term of use",
						"type": "web_url",
						"url": "www.google.com"
					},
					{
						"title":"Help",
						"type":"postback",
						"payload":"HELP_PAYLOAD"
					}
				]}
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
				"title":"Financial",
				"type":"nested",
				"call_to_actions":[					
					{
						"title":"Balance Enquiry",
						"type":"postback",    
						"payload":"BALANCE_ENQUIRY_PAYLOAD"
					},
					{
						"title":"Mini Statement",
						"type":"postback",
						"payload":"MINI_STATEMENT_PAYLOAD"
					},
					{
						"title":"Loan Outstanding",
						"type":"postback",
						"payload":"LOAN_OUTSTANDING_PAYLOAD"
					},
					{
						"title":"Payment Schedule",
						"type":"postback",
						"payload":"PAYMENT_SCHEDULE_PAYLOAD"    
					}
				]
			},
			{
				"title":"Non-Financial",
				"type":"nested",
				"call_to_actions":[
					{
						"title":"Product",
						"type":"postback",    
						"payload":"PRODUCT_PAYLOAD"
					},
					{	
						"title":"Exchange Rate",
						"type":"postback",    
						"payload":"EXCHANGE_RATE_PAYLOAD"
					},
					{
						"title":"Branch and ATM location",
						"type":"postback",    
						"payload":"BRANCH_ATM_PAYLOAD"
					}
				]
			},
			{
				"title":"Contact Us",
				"type":"postback",
				"payload":"CONTACT_US_PAYLOAD"
			}
	   ]
	}
  ]
})
requests.post(url=url_messenger_profile, params=params, headers=headers, data=persistent_menu_data)

@page.callback(['HELP_PAYLOAD'])
def click_help_payload(payload, event):
	page.send(event.sender_id, "clicked help")

@page.callback(['CONTACT_US_PAYLOAD'])
def click_help_payload(payload, event):
	page.send(event.sender_id, "contact us")

@page.callback(['CHECK_BALANCE_PAYLOAD'])
def click_check_balance_payload(payload, event):
	page.send(event.sender_id, 'click check balance')

@page.callback(['BRANCH_ATM_PAYLOAD'])
def click_branch_atm_payload(payload, event):
	print 'location access'
	print "id ", event.sender_id
	location_request = json.dumps({
		"recipient":{
			"id": event.sender_id
		},
		"message":{
			"text": "Please send me your current location now. I will help find the nearest Branch and ATM for you.",
			"quick_replies":[{
				"content_type":"location"
			}]	
		}
	})
	print "json: %s", location_request
	requests.post(url=url_messenger_message, params=params, headers=headers, data=location_request)
	print "data: ",data

@page.callback(['PRODUCT_PAYLOAD'])
def click_product_payload(payload, event):
	page.typing_on(event.sender_id)
	
	quick_replies = [{'title': 'Loan', 'payload': 'LOAN_ACTION'},
				{'title': 'Saving', 'payload': 'SAVING_ACTION'}]

	page.send(event.sender_id, 
		  "What kind of product do you prefer?",
		  quick_replies=quick_replies,
		  metadata="DEVELOPER_DEFINED_METADATA", notification_type=NotificationType.REGULAR)
	page.typing_off(event.sender_id)

@page.callback(['LOAN_ACTION'])
def click_loan_action(payload, event):
	page.typing_on(event.sender_id)
	quick_replies = [{'title': 'Business Loan', 'payload': 'LOAN_ACTION'},
				{'title': 'Consumption Loan', 'payload': 'SAVING_ACTION'},
				{'title': 'Home Improvment Loan', 'payload':'SAVING_ACTION'},
				{'title': 'Agriculture Loan', 'payload':'SAVING_ACTION'},
				{'title': 'SME Loan', 'payload':'SAVING_ACTION'},
				{'title': 'Working Captital Loan', 'payload':'SAVING_ACTION'},
				{'title': 'Personal Loan', 'payload':'SAVING_ACTION'},
				{'title': 'Solar Loan', 'payload':'SAVING_ACTION'},
				{'title': 'Education Loan', 'payload':'SAVING_ACTION'},
				{'title': 'Community Bank Loan', 'payload':'SAVING_ACTION'},
				{'title': 'Loan Payment Service Via Truemoney Agent', 'payload':'SAVING_ACTION'}]
	page.send(event.sender_id, 
		  "What kind of product do you prefer?",
		  quick_replies=quick_replies,
		  metadata="DEVELOPER_DEFINED_METADATA", notification_type=NotificationType.REGULAR)

	page.typing_off(event.sender_id)

@page.callback(['SAVING_ACTION'])
def click_loan_action(payload, event):
	page.send(event.sender_id, "saving action")
	print 'test'
