from admin.views.baseview import *
from flask_babel import lazy_gettext as _

class PageView(AdminSecureView):
    """
    PageView
    """
    @route('/index.html', methods=['GET'])
    def index(self):
        return render_template('/page/index.html')


PageView.register(admin_blueprint)