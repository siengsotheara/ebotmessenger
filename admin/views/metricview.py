from admin.views.baseview import *
from core.logics.broadcast import broadcasts, Broadcast
from core.logics.user import users
from core.logics.broadcastmessage import broadcastmessages, BroadcastMessage
from flask_babel import lazy_gettext as _

class MetricTable(Table):
	rowno               = RowNumberColumn(_('#'))
	broadcast_id        = LinkColumn(_('BROADCAST ID'), render_kw= {'link': 'graph.html/'})
	message_creative_id = Column(_('MESSAGE CREATIVE ID'))
	messaging_type      = Column(_('MESSAGING TYPE'))
	tag                 = Column(_('TAG'))
	notification_type   =  Column(_('NOTIFICATION TYPE'))
	create_by           = Column(_('CREATE BY'))
	create_at           = DateTimeColumn(_('CREATE DATE'))

class MetricView(AdminSecureView):

	@route('/index.html')
	def index(self):
		table = MetricTable(data=broadcasts._search())
		return render_template('/metric/index.html', table=table, username=users.current_user().username)

	@route('/graph.html/<pid>', methods=['GET', 'POST'])
	def graph(self, pid):
		name        = None
		period      = None
		value       = None
		metrics     = None
		title       = None
		description = None
		id          = None

		headers = {'Content-Type':'application/json'}
		params = {
			"access_token": FACEBOOK_TOKEN
		}
		result = requests.get(url='https://graph.facebook.com/v2.11/{0}/insights/messages_sent'.format(pid), params=params)
		if result.status_code == requests.codes.ok:
			name        = result.json()['data'][0]['name']
			period      = result.json()['data'][0]['period']
			value       = result.json()['data'][0]['values'][0]['value']
			metrics     = pid
			title       = result.json()['data'][0]['title']
			description = result.json()['data'][0]['description']
			id          = result.json()['data'][0]['id']
		return render_template('/metric/graph.html', 
						 metrics=metrics,
						 id=id,
						 value=value,
						 period=period,
						 title=title,
						 description=description,
						 name=name,
						 username=users.current_user().username)

MetricView.register(admin_blueprint)