from admin.views.baseview import *
import datetime

class HomeView(AdminSecureView):
    
    @route('/index.html')
    def index(self):
        return render_template('home/index.html')

    @route('/dashboard.html')
    def dashboard(self):
        return redirect(url_for('admin.HomeView:index'))

    @route('/change_language/<code>', methods=['GET','POST'])
    def change_language(self, code):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=7300)
        resp = make_response(redirect('language/%s' % code))
        resp.set_cookie('language', code, expires=expire_date)
        return resp

HomeView.register(admin_blueprint)