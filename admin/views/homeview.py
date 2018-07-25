from admin.views.baseview import *

class HomeView(RestSecureView):
    
    @app.route('/')
    def index(self):
        return render_template(
            'home/index.html'
            
        )



HomeView.register(admin_blueprint)