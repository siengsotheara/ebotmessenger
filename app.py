import os 
from flask import Flask, request, render_template, redirect, url_for
from fbmq import Page, Template
from config import SECRET_KEY, RECAPTCHA_PUBLIC_KEY, ProductConfig

from flask_material import Material  
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required


page = Page(ProductConfig.FACEBOOK_TOKEN)
app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY


Material(app)
app.config.setdefault('MATERIAL_SERVE_LOCAL', True)

# straight from the wtforms docs:
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')

class ExampleForm(Form):
    field1 = TextField('First Field', description='This is field one.')
    field2 = TextField('Second Field', description='This is field two.',
                       validators=[Required()])
    hidden_field = HiddenField('You cannot see this', description='Nope')
    recaptcha = RecaptchaField('A sample recaptcha field')
    radio_field = RadioField('This is a radio field', choices=[
        ('head_radio', 'Head radio'),
        ('radio_76fm', "Radio '76 FM"),
        ('lips_106', 'Lips 106'),
        ('wctr', 'WCTR'),
    ])
    checkbox_field = BooleanField('This is a checkbox',
                                  description='Checkboxes can be tricky.')

    # subforms
    mobile_phone = FormField(TelephoneForm)

    # you can change the label as well
    office_phone = FormField(TelephoneForm, label='Your office phone')

    ff = FileField('Sample upload')

    submit_button = SubmitField('Submit Form')


    def validate_hidden_field(self, form, field):
        raise ValidationError('Always wrong')

@app.route('/form')
def test_form():
    form = ExampleForm()   
    return render_template('test.html', form = form) 

@app.route('/')
def index():
    return redirect(url_for('payment'))

@app.route('/payment')
def payment():
    return render_template('payment.html')


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

# @page.handle_message
# def handle_message(event):
#     pass

# @page.after_send
# def after_send(payload, response):
#     print response


# import thread_settings

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run('0.0.0.0', port)
