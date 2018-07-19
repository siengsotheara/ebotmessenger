from app import FACEBOOK_TOKEN, CASA_LINK
from app import json, page, requests, data, QuickReply

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

page.greeting("Hello {{user_full_name}} I'm PhillipBot. Thank for getting in touch with us on Messenger. Please send us any questions you may have")


page.show_starting_button("START_PAYLOAD")

@page.callback(['START_PAYLOAD'])
def start_payload_callback(payload, event):
	sender_id = event.sender_id
	page.typing_on(sender_id)
	#page.send(sender_id, u"Welcome! Nice to see you here. I'm KREDIT Chatbot and I will help you response quickly as an option menu below.")
	#page.send(sender_id, u"Welcome to KREDIT MFI Plc. With this chatbot you can do whatever you want.")
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

@page.callback(['PRODUCT_PAYLOAD'])
def click_product_payload(payload, event):
	page.typing_on(event.sender_id)
	page.send(event.sender_id, 'PRODUCT_PAYLOAD')
	
	quick_replies = [{'title': 'Loan', 'payload': 'LOAN_ACTION'},
				{'title': 'Saving', 'payload': 'SAVING_ACTION'}]

	page.send(event.sender_id, 
		  "What kind of product do you prefer?",
		  quick_replies=quick_replies,
		  metadata="DEVELOPER_DEFINED_METADATA")
	page.typing_off(sender_id)
	print("you clicked %s menu" % payload)

@page.callback(['LOAN_ACTION'])
def click_loan_action(payload, event):
	page.send(event.sender_id, "loan action")
	print 'test'

@page.callback(['SAVING_ACTION'])
def click_loan_action(payload, event):
	page.send(event.sender_id, "saving action")
	print 'test'
