from admin.views.baseview import *
from core.logics.broadcast import broadcast, BroadcastMessage


#class UserFilterForm(Form):
#    search = TextField(
#        _(u'Search'),
#        render_kw={
#            'placeholder':_(u'search')
#        }
#    )

#class UserForm(Form):
#    name = TextField(
#        _(u'Username'),
#        render_kw = {
#            'data-val':'true',
#            'data-val-required':u'Input Required'
#            }
#        )
#    full_name = TextField(
#        _(u'Full Name'),
#        render_kw = {
#            'data-val':'true',
#            'data-val-required':u'Input Required'
#            }
#        )
#    province_code = DynamicSelectField(
#        _(u'Province'),
#        allow_blank = True,
#        blank_text = '',
#        query_factory = provinces.all,
#        get_label = 'name',
#        render_kw = {
#            'required':'required'
#        }
#    )
class BroadcastView(AdminSecureView):
    
    @route('/broadcast')
    def index(self):
        return render_template('/broadcast/index.html')

BroadcastView.register(admin_blueprint)