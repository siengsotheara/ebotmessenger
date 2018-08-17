from admin.views.baseview import *
from core.logics.broadcast import broadcasts, Broadcast
from core.logics.user import users
from core.logics.broadcastmessage import broadcastmessages, BroadcastMessage
from core.logics.page import pages
from flask_babel import lazy_gettext as _

class DynamicTextForm(FlaskForm):
	token        = TextField(_('Token'), render_kw = {'class':'form-control', 'placeholder':_('Token'), 'required':'required'})
	text          = TextAreaField(_('Text'), render_kw = {'class':'form-control', 'rows':'3', 'placeholder': _('text'), 'required':'required'})

class VideoImageForm(FlaskForm):
	token        = TextField(_('Token'), render_kw = {'class':'form-control', 'placeholder':_('Token'), 'required':'required'})
	url          = TextField(_('URL'), render_kw = {'class':'form-control', 'placeholder': _("URL"), 'required':'required'})
	share_url    = TextField(_('Content URL'), render_kw = {'class':'form-control', 'placeholder': _("Share URL for Facebook's video content"), 'required':'required', 'value':'https://www.facebook.com/sharer/sharer.php?u='})
	button_title = TextField(_('Share'), render_kw = {'class':'form-control', 'placeholder': _("Button's title"), 'required':'required', 'value':'Share'}) 

class TextButtonShareForm(FlaskForm):
	token        = TextField(_('Token'), render_kw = {'class':'form-control', 'placeholder':_('Token'), 'required':'required'})
	text = TextAreaField(_('Text'), render_kw = {'class':'form-control', 'rows':'5', 'placeholder': _('text'), 'required':'required'})
	url = share_url    = TextField(_('Content URL'), render_kw = {'class':'form-control', 'placeholder': _("Share URL for Facebook's video content"), 'required':'required', 'value':'https://www.facebook.com/sharer/sharer.php?u='})
	button_title = TextField(_('Share'), render_kw = {'class':'form-control', 'placeholder': _("Button's title"), 'required':'required', 'value':'Share'}) 

class DynamicTextTable(Table):
	rowno                 = RowNumberColumn(_('#'))
	message_creative_id   = Column(_('MESSAGE CREATIVE ID'))
	message_creative_type = Column(_('MESSAGE CREATIVE TYPE'))
	content               = Column(_('CONTENT'))
	is_already_broadcast  = Column(_('BROADCAST'))
	create_by             = Column(_('CREATE BY'))
	create_at             = DateTimeColumn(_('CREATE DATE'))

class BroadcastView(AdminSecureView):
	"""
	BroadcastView
	"""

	@route('/index.html')
	def index(self):
		table = DynamicTextTable(data=broadcastmessages._search())
		return render_template('/broadcast/index.html', table=table, username=users.current_user().username)

class DynamicTextView(AdminSecureView):
	"""
	DynamicTextView
	"""

	@route('/index.html')
	def index(self):
		table = DynamicTextTable(data=[])
		form  = DynamicTextForm()
		p = pages._findByKey('ACCESS_TOKEN')
		if p:
			form.token.data = p.value

		return render_template('/broadcast/dynamictext/index.html', form=form, table=table, username=users.current_user().username)

	@route('/add.html', methods = ['GET', 'POST'])
	def add(self):
		form  = DynamicTextForm()
		table = DynamicTextTable(data=[])
		error = None

		if request.method == 'GET':
			return redirect(url_for('admin.DynamicTextView:index'))

		if form.validate_on_submit():
			headers = {'Content-Type':'application/json'}
			params = {
				"access_token": form.token.data
			}
			datas = json.dumps({
				'messages': [{
					'dynamic_text': {
						'text': u'{0}'.format(form.text.data),
						'fallback_text': 'Please Contact Tel. 023 930 000 for more information'
					}
				}]
			})

			message_creative = requests.post(url='https://graph.facebook.com/v2.11/me/message_creatives', headers=headers, params=params, data=datas)

			if message_creative.status_code ==  requests.codes.ok:
				notification_type = request.form.get('notification_type', 'REGULAR')
				is_broadcast_now = 'N'
				
				if request.form.get("broadcast_now"):
					is_broadcast_now = 'Y'
				
				obj = BroadcastMessage()
				obj.is_already_broadcast = is_broadcast_now
				obj.message_creative_id = message_creative.json().get('message_creative_id', 0)
				obj.message_creative_type = 'text'
				obj.content = u'{0}'.format(form.text.data)
				broadcastmessages._insert(obj)
				
				if is_broadcast_now == 'Y':
					datas = json.dumps({    
						'message_creative_id': message_creative.json().get('message_creative_id', 0),
						'notification_type': notification_type,
						'messaging_type': 'MESSAGE_TAG',
						'tag': 'NON_PROMOTIONAL_SUBSCRIPTION'
					})

					broadcast_messages = requests.post(url='https://graph.facebook.com/v2.11/me/broadcast_messages', headers=headers, params=params, data=datas)
					if broadcast_messages.status_code == requests.codes.ok:
						d = json.loads(datas)
						obj = Broadcast()
						obj.broadcast_id = broadcast_messages.json().get('broadcast_id', 0)
						obj.message_creative_id = message_creative.json().get('message_creative_id', 0)
						obj.tag = d['tag']
						obj.notification_type = notification_type
						obj.messaging_type = d['messaging_type']
						broadcasts._insert(obj)
						return redirect(url_for('admin.BroadcastView:index'))
			else:
				error = message_creative.json()['error']['message']

		return render_template('/broadcast/dynamictext/index.html', form=form, username=users.current_user().username, error=error)

class VideoImageView(AdminSecureView):
	"""
	VideoImageView
	"""

	@route('/index.html')
	def index(self):
		form = VideoImageForm()
		p = pages._findByKey('ACCESS_TOKEN')
		if p:
			form.token.data = p.value
		return render_template('/broadcast/videoimage/index.html', form=form, error=None, username=users.current_user().username)

	@route('/add.html', methods = ['GET', 'POST'])
	def add(self):
		form  = VideoImageForm()
		error = None

		if request.method == 'GET':
			return redirect(url_for('admin.VideoImageView:index'))

		if form.validate_on_submit():
			media_type = request.form.get('media_type', 'video')
			headers = {'Content-Type':'application/json'}
			params  = {
				"access_token": form.token.data
			}
			
			datas   = json.dumps(
			{
				'messages':[{
					'attachment':{
						'type':'template',
						'payload': {
							'template_type':'media',
							'elements':[{
								'media_type': media_type,
								'url':u'{0}'.format(form.url.data),
								'buttons':[{
									'type':'web_url',
									'url': u'{0}'.format(form.share_url.data),
									'title': u'{0}'.format(form.button_title.data),
									'webview_height_ratio':'full'
									}]
								}]
							}
						}
					}]
			})
			
			message_creative = requests.post(url='https://graph.facebook.com/v2.11/me/message_creatives', headers=headers, params=params, data=datas)

			if message_creative.status_code ==  requests.codes.ok:
				notification_type = request.form.get('notification_type', 'REGULAR')
				is_broadcast_now = 'N'
				
				if request.form.get("broadcast_now"):
					is_broadcast_now = 'Y'
				
				obj = BroadcastMessage()
				obj.is_already_broadcast = is_broadcast_now
				obj.message_creative_id = message_creative.json().get('message_creative_id', 0)
				obj.message_creative_type = media_type
				broadcastmessages._insert(obj)
				
				if is_broadcast_now == 'Y':
					datas = json.dumps({    
						'message_creative_id': message_creative.json().get('message_creative_id', 0),
						'notification_type': notification_type,
						'messaging_type': 'MESSAGE_TAG',
						'tag': 'NON_PROMOTIONAL_SUBSCRIPTION'
					})

					broadcast_messages = requests.post(url='https://graph.facebook.com/v2.11/me/broadcast_messages', headers=headers, params=params, data=datas)
					if broadcast_messages.status_code == requests.codes.ok:
						d = json.loads(datas)
						obj = Broadcast()
						obj.broadcast_id = broadcast_messages.json().get('broadcast_id', 0)
						obj.message_creative_id = message_creative.json().get('message_creative_id', 0)
						obj.tag = d['tag']
						obj.notification_type = notification_type
						obj.messaging_type = d['messaging_type']
						broadcasts._insert(obj)
						return redirect(url_for('admin.BroadcastView:index'))
					else:
						error = message_creative.json()['error']['message']
			else:
				error = message_creative.json()['error']['message']

		return render_template('/broadcast/videoimage/index.html', form=form, error=error, username=users.current_user().username)


class TextButtonShareView(AdminSecureView):
	"""
	TextButtonShareView
	"""

	@route('/index.html', methods = ['GET'])
	def index(self):
		form  = TextButtonShareForm()
		error = None
		p = pages._findByKey('ACCESS_TOKEN')
		if p:
			form.token.data = p.value
		return render_template('/broadcast/textbuttonshare/index.html', form=form, username=users.current_user().username, error=error)

	@route('/add.html', methods = ['GET', 'POST'])
	def add(self):
		form  = TextButtonShareForm()
		error = None

		if request.method == 'GET':
			return redirect(url_for('admin.TextButtonShareView:index'))

		if form.validate_on_submit():
			headers = {'Content-Type':'application/json'}
			params  = {
				"access_token": form.token.data
			}
			
			datas   = json.dumps(
			{
				'messages': [{
					'attachment': {
						'type': "template",
						'payload': {
						'template_type':'button',
						'text': u'{0}'.format(form.text.data),
						'buttons':[{
							'type':'web_url',
							'url': u'{0}'.format(form.share_url.data),
							"title":u'{0}'.format(form.button_title.data),
							'webview_height_ratio': 'full'
							}]
						}
					}    
				}]
			})
			
			message_creative = requests.post(url='https://graph.facebook.com/v2.11/me/message_creatives', headers=headers, params=params, data=datas)

			if message_creative.status_code ==  requests.codes.ok:
				notification_type = request.form.get('notification_type', 'REGULAR')
				is_broadcast_now = 'N'
				
				if request.form.get("broadcast_now"):
					is_broadcast_now = 'Y'
				
				obj = BroadcastMessage()
				obj.is_already_broadcast = is_broadcast_now
				obj.message_creative_id = message_creative.json().get('message_creative_id', 0)
				obj.message_creative_type = 'text button'
				broadcastmessages._insert(obj)
				
				if is_broadcast_now == 'Y':
					datas = json.dumps({    
						'message_creative_id': message_creative.json().get('message_creative_id', 0),
						'notification_type': notification_type,
						'messaging_type': 'MESSAGE_TAG',
						'tag': 'NON_PROMOTIONAL_SUBSCRIPTION'
					})

					broadcast_messages = requests.post(url='https://graph.facebook.com/v2.11/me/broadcast_messages', headers=headers, params=params, data=datas)
					if broadcast_messages.status_code == requests.codes.ok:
						d = json.loads(datas)
						obj = Broadcast()
						obj.broadcast_id = broadcast_messages.json().get('broadcast_id', 0)
						obj.message_creative_id = message_creative.json().get('message_creative_id', 0)
						obj.tag = d['tag']
						obj.notification_type = notification_type
						obj.messaging_type = d['messaging_type']
						broadcasts._insert(obj)
						return redirect(url_for('admin.BroadcastView:index'))
					else:
						error = message_creative.json()['error']['message']
			else:
				error = message_creative.json()['error']['message']

		render_template('/broadcast/textbuttonshare/index.html', form=form, error=error, username=users.current_user().username)

BroadcastView.register(admin_blueprint)
DynamicTextView.register(admin_blueprint)
VideoImageView.register(admin_blueprint)
TextButtonShareView.register(admin_blueprint)