from fbmq import Template
from app import page, ProductConfig
import sys
import requests


thread_settings_url = 'https://graph.facebook.com/v2.6/me/messenger_profile'
token = ProductConfig.FACEBOOK_TOKEN

params = {
    "access_token": token
}
headers = {
    "Content-Type": "application/json"
}

def log(str):  # simple wrapper for logging to stdout on heroku
    print str(str)
    sys.stdout.flush()

# Greeting text
page.greeting("Hi {{user_full_name}} Welcome to Find Me Bot! My Mission is help you to easy find the pitch. :)")

page.show_starting_button("START")

@page.callback(['START'])
def start_callback(payload, event):
    sender_id = event.sender_id
    page.typing_on(sender_id)
    page.send(sender_id, "Welcome to EBot Messenger. What can I help you?")
    page.typing_off(sender_id)
    print("Let's start! %s", sender_id)

# page.show_persistent_menu([Template.ButtonPostBack('My Account', 'MY_ACCOUNT'),
#                            Template.ButtonPostBack('News', 'NEWS'),
#                            Template.ButtonPostBack('Help', 'HELP')])

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
      "locale":"zh_CN",
      "composer_input_disabled":true,
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

@page.callback(['MY_ACCOUNT'])
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

@page.callback(['HELP'])
def click_persistent_menu_help(payload, event):
    sender_id = event.sender_id
    page.send(sender_id, "you clicked %s menu" % payload)
    print("you clicked %s menu" % payload)

