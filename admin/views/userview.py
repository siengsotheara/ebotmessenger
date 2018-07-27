from admin.views.baseview import *
from core.models import User
#from core.logics.users import users
from flask_babel import lazy_gettext as _

class UserFilterForm(Form):
    search = TextField(
        _(u'Search'),
        render_kw={
            'placeholder':_(u'search')
        }
    )

class UserForm(Form):
    name = TextField(
        _(u'Username'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required'
            }
        )
    full_name = TextField(
        _(u'Full Name'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required'
            }
        )
    email = TextField(
        _(u'Email'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required'
            }
        )
    password = PasswordField(
        _(u'Password'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required'
            }
        )
    confirm_password = PasswordField(
        _(u'Confirm Password'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required',
            'data-val-remote':u'Password Incorrect',
            'data-val-remote-additionalfields':'password,confirm_password',
            'data-val-remote-url':'users/confirm_password'
            }
        )

class ChangePasswordForm(FlaskForm):
    name = TextField(
        _(u'Username'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required'
            }
        )
    old_password = PasswordField(
        _(u'Password (Old)'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required'
            }
        )
    password = PasswordField(
        _(u'New Password'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required'

            }
        )
    confirm_password = PasswordField(
        _(u'Confirm Password (New)'),
        render_kw = {
            'data-val':'true',
            'data-val-required':u'Input Required',
            'data-val-remote':u'Password Incorrect',
            'data-val-remote-additionalfields':'password,confirm_password',
            'data-val-remote-url':'users/confirm_password'
            }
        )

class UserTable(Table):
    rowno = RowNumberColumn(_(u'No.'))
    name = Column(_(u'Username'))
    full_name = Column(_(u'Full Name'))
    email = Column(_(u'Email'))
    action = LamdaColumn('', get_value=lambda row:
                            '<a href="%s" class="action edit">Edit</a> \
                             <a href="%s" class="action delete">Delete</a>' \
                            % (url_for('admin.UserView:edit', id=row.id),
                               url_for('admin.UserView:delete', id=row.id) ))

class UserView(AdminSecuredView):
    route_base = '/users'

    def index(self):
        form = UserFilterForm()
        table = UserTable()

        # Load filter from session
        filter_data = json.loads(get_session('users/filter', '{}'), object_pairs_hook=load_with_datetime) 
        for k, v in filter_data.iteritems():
            if hasattr(form, k):
                getattr(form, k).data = v

        return render_template(
            'users/index.html',
            title = _('User List'),
            form = form,
            table = table
         )

    @route('/filter', methods=['GET' , 'POST'])
    def filter(self):
        form = UserFilterForm()
        q = users.search(**form.data)
        pagging = DataView(query=q)
        table = UserTable(data=pagging.result)

        # Keep filter in session
        filter_data = json.dumps(form.data, cls=ExtEncoder)
        set_session('users/filter', filter_data)

        return render_template(
            'users/filter.html',
            data = pagging.result,
            table = table,
            pagging = pagging
        )

    @route('/add', methods = ['GET' , 'POST'])
    def add(self):
        form = UserForm()

        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            users.add(user)
            return redirect(url_for('admin.UserView:index'))

        return render_template(
            'users/add.html',
            title = _(u'Add Users'),
            form = form
        )

    @route('/edit/<int:id>', methods=['GET' , 'POST'])
    def edit(self,id):
        user = users.find(id = id)
        form = UserForm(obj=user)

        if form.validate_on_submit():
            user.name = form.name.data
            user.full_name = form.full_name.data
            user.email = form.email.data
            users.update(user)
            return redirect(url_for('admin.UserView:index'))

        return render_template(
            'users/edit.html',
            title = _(u'Edit Users Login'),
            form = form,
            id = id
         )

    @route('/delete/<int:id>', methods=['GET' , 'POST'])
    def delete(self,id):
        user = users.find(id)
        form = UserForm(obj=user)

        if form.validate_on_submit():
            user.name = form.name.data
            user.full_name = form.full_name.data
            user.email = form.email.data
            users.remove(user)
            return redirect(url_for('admin.UserView:index'))

        return render_template(
            'users/delete.html',
            title = _(u'Delete Users'),
            form = form,
            id = id
        )

    # Remote
    @route('/confirm_password', methods=['GET','POST'])
    def confirm_password(self):

        password = request.args.get('password')
        confirm_password = request.args.get('confirm_password')

        if password == confirm_password:
            return json.dumps(True)
        else:
            return json.dumps(False)

    @route('/change_password/<int:id>', methods=['GET' , 'POST'])
    def change_password(self,id):
        form = ChangePasswordForm()

        if not form.is_submitted():
            user = users.find(id = id)
            form.name.data = user.name

        if form.validate_on_submit():
             user = users.authenticate(form.name.data, form.old_password.data)
             if user:
                 user.password = form.password.data
                 users.change_password(user)
                 return  redirect(url_for('admin.UserView:index'))

        return render_template(
            'users/change_password.html',
            title = _('Edit Password Login'),
            form = form,
            id = id
        )

UserView.register(admin_blueprint)