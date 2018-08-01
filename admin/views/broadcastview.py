from admin.views.baseview import *
from core.logics.broadcast import broadcast, BroadcastMessage
from flask_babel import lazy_gettext as _

class DynamicTextForm(FlaskForm):
	text = TextAreaField(_('Text'), render_kw = {'class':'form-control', 'rows':'3', 'placeholder': _('text'), 'required':'required'})
	fallback_text = TextAreaField(_('Fallback Text'), render_kw = {'class':'form-control', 'rows':'3', 'placeholder': _('fallback text'), 'required':'required'})

class DynamicTextTable(Table):
	rowno = RowNumberColumn(_(u'Nº'), render_kw={'width':'20%'})
	message_id = Column(_('MESSAGE ID'))
	other = Column(_('OTHER'))

class BroadcastView(AdminSecureView):
	@route('/index.html')
	def index(self):
		table = DynamicTextTable(data=[])
		return render_template('/broadcast/index.html', table=table)

class DynamicTextView(AdminSecureView):
	@route('/index.html')
	def index(self):
		table = DynamicTextTable(data=[])
		form = DynamicTextForm()
		return render_template('/broadcast/dynamictext/index.html', form=form, table=table)

	@route('/add.html', methods = ['POST'])
	def add(self):
		form = DynamicTextForm()
		table = DynamicTextTable(data=[])
		if form.validate_on_submit():
			
			headers = {'Content-Type':'application/json'}
			params = {
				"access_token": FACEBOOK_TOKEN
			}
			datas=json.dumps({
				"messages": [{
					"dynamic_text": {
						"text": form.text.data,
						"fallback_text": form.fallback_text.data
					}
				}]
			})

			message_creative = requests.post(url='https://graph.facebook.com/v2.11/me/message_creatives', headers=headers, params=params, data=datas)
			if message_creative.status_code ==  requests.codes.ok:
				print message_creative.json()['message_creative_id']
				return redirect(url_for('admin.BroadcastView:index'))

			return redirect(url_for('admin.BroadcastView:index'))
		return render_template('/broadcast/dynamictext/index.html', form=form)

class ImageView(AdminSecureView):
	@route('/index.html')
	def index(self):
		return render_template('/broadcast/image/index.html')

class VideoView(AdminSecureView):
	@route('/index.html')
	def index(self):
		return render_template('/broadcast/video/index.html')


BroadcastView.register(admin_blueprint)
DynamicTextView.register(admin_blueprint)
ImageView.register(admin_blueprint)
VideoView.register(admin_blueprint)