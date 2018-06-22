import os 
from flask import Flask, request
from fbmq import Page, Template
from config import ProductConfig

page = Page(ProductConfig.FACEBOOK_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return 'ok'

@app.route('/webhook', methods=['GET'])
def validate():
    if request.args.get('hub.mode', '') == 'subscribe' and \
                    request.args.get('hub.verify_token', '') == ProductConfig.VERIFY_TOKEN:

        print("Validating webhook")

        return request.args.get('hub.challenge', '')
    else:
        return 'Failed validation. Make sure the validation tokens match.'

@app.route('/webhook', methods=['POST'])
def webhook():
    print request.get_json()
    page.handle_webhook(request.get_data(as_text=True))
    return "ok"

@page.handle_message
def handle_message(event):
    pass

@page.after_send
def after_send(payload, response):
    print response

import thread_settings

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port)
