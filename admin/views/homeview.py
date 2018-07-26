from admin.views.baseview import *
import datetime

class HomeView(AdminSecureView):
    
    @route('/')
    def index(self):
        return render_template('home/index.html')

    @route('/change_language/<code>', methods=['GET','POST'])
    def change_language(self, code):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=7300)
        resp = make_response(redirect('language/%s' % code))
        resp.set_cookie('language', code, expires=expire_date)
        return resp

    def dashboard(self):
        #total_suppliers = suppliers.count()
        #total_users = users.count()
        #suppliers_statistic = suppliers.statistic()
        #systems_statistic = systems.statistic()
        #status_statistic = status.statistic(user_id=get_session('user_id', 0))

        return render_template(
            'home/dashboard.html',
            title = 'Dashboard'
        )

HomeView.register(admin_blueprint)