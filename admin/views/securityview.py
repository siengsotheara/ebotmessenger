from admin.views.baseview import *
from core.logics.user import users
from flask_babel import lazy_gettext as _
from urlparse import urlparse, urljoin

class LoginForm(FlaskForm):
	username = TextField(
		_(u'Username'),
		render_kw = {
			'placeholder':_(u'Username'),
			'data-val':'true',
			'data-val-required':_(u'Input Required'),
			'class':'form-control'
		}
	)

	password = PasswordField(
		_(u'Password'),
		render_kw = {
			'placeholder':_(u'Password'),
			'data-val':'true',
			'data-val-required':_(u'Input Required'),
			'class':'form-control'
		}
	)
	target = HiddenField(_('Target'))


class SecurityView(AdminView):
	route_base = '/security'
	
	@route('/login.html', methods=['GET', 'POST'])
	def login(self):		
		form  = LoginForm()
		error = None

		if 'username' in session:
			return redirect(url_for('admin.HomeView:index'))

		if request.method == 'GET':
			form.target.data = request.args.get("next", url_for('admin.HomeView:index'))

		if form.validate_on_submit():
			user = users.authenticate(form.username.data, form.password.data)
			if user:
				set_session('username', user.username)
				return redirect(form.target.data or url_for('admin.HomeView:index'))
			else:
				error = _('Username or password you entered is incorrect.')
			
		return render_template(
			'security/login.html',
			title=_(u'Login'),
			form=form,
			error=error)

	def logout(self):
		session.clear()
		return redirect(url_for('admin.SecurityView:login'))

SecurityView.register(admin_blueprint)