from admin.views.baseview import *
from core.logics.broadcast import broadcasts, Broadcast
from core.logics.broadcastmessage import broadcastmessages, BroadcastMessage
from flask_babel import lazy_gettext as _

class MetricTable(Table):
	rowno = RowNumberColumn(_('#'))
	broadcast_id = LinkColumn(_('BROADCAST ID'), render_kw= {'link': 'open.html/'})
	message_creative_id = Column(_('MESSAGE CREATIVE ID'))
	messaging_type = Column(_('MESSAGING TYPE'))
	tag = Column(_('TAG'))
	notification_type =  Column(_('NOTIFICATION TYPE'))
	create_by = Column(_('CREATE BY'))
	create_at = DateTimeColumn(_('CREATE DATE'))

class MetricView(AdminSecureView):

	@route('/index.html')
	def index(self):
		table = MetricTable(data=broadcasts._search())
		return render_template('/metric/index.html', table=table)

	@route('/open.html/<id>', methods=['GET', 'POST'])
	def open(self, id):
		return render_template('/metric/open.html')

MetricView.register(admin_blueprint)