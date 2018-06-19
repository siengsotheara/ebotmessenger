import requests
import json

from H203.fb import app
from H203.core.logics.suppliers import SupplierLogic

thread_settings_url = 'https://graph.facebook.com/v2.6/me/messenger_profile'
token = app.config['TESTING_TOKEN']
domain = app.config['DOMAIN_NAME']

params = {
    "access_token": token
}
headers = {
    "Content-Type": "application/json"
}
#Add gretting text
greeting_text_data = json.dumps({
  "greeting":[
    {
      "locale":"default",
      "text":"សូមស្វាគម៍មកកាន់កម្មវិធីរបស់យើង។ជាមួយកម្មវិធីនេះអាចជួយដោះស្រាយបញ្ហាលោកអ្នកក្នុងការបង់បង់វិក័យបត្រផ្សេងៗ"
    }
  ] 
})
requests.post(thread_settings_url, params=params, headers=headers, data=greeting_text_data)

#Add get start button
get_started_data = json.dumps({ 
  "get_started":{
    "payload":"GET_STARTED"
  }
})
requests.post(thread_settings_url, params=params, headers=headers, data=get_started_data)

#add persistent_menu
#get service
service_type_list = SupplierLogic().find_children()
main_menus = []
for service_type in service_type_list:
    qr = service_type.ext.get('bot')
    if service_type.children:
        main_menu = {
                        "title":u"បង់វិក័យបត្រ",
                        "type":"nested",
                        "call_to_actions" : []
                    }
        for s in service_type.children:
            #service
            sqr = s.ext.get('bot')
            if s.__class__.__name__=='ServiceType':
                if s.children:
                    #supplier
                    submenu = {
                                "title":sqr.get('qr_text'),
                                "type":"nested",
                                "call_to_actions" : []
                                }
                    for supplier in s.children:
                        nsqr = supplier.ext.get('bot')
                        next_submenu = {
                                        "title":nsqr.get('qr_text'),
                                        "type":"postback",
                                        "payload":"SUPPLIER_%s" %supplier.id
                                        }
                        submenu['call_to_actions'].append(next_submenu)
                    main_menu['call_to_actions'].append(submenu)
                else:
                    submenu = {
                                    "title":sqr.get('qr_text'),
                                    "type":"postback",
                                    "payload":"SERVICE_%s" %s.id
                                    }
                    main_menu['call_to_actions'].append(submenu)

        main_menus.append(main_menu)
        break

fixed_main_menu = [
                {
                    "type":"postback",
                    "title":u"ទំនាក់ទំនង",
                    "payload":"CONTACT"
                },
                {
                    "type":"postback",
                    "title":u"ជំនួយ",
                    "payload":"HELP"
                }
            ]

main_menus += fixed_main_menu

persistent_menu_data = json.dumps({
  "persistent_menu":[
    {
      "locale":"default",
      "composer_input_disabled":False,
      "call_to_actions":main_menus
    }
  ]
})
requests.post(thread_settings_url, params=params, headers=headers, data=persistent_menu_data)

#add domain to white list
white_list = json.dumps({
  "whitelisted_domains":[
    domain
  ]
})
requests.post(thread_settings_url, params=params, headers=headers, data=white_list)
