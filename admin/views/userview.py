from admin.views.baseview import *
from flask_babel import lazy_gettext as _
from core.logics.user import users, User

class ChangePasswordForm(FlaskForm):
    username = TextField(_('Username'), render_kw = {'class':'form-control', 'placeholder': _("Username"), 'required':'required', 'disabled':'disabled'})
    password =  PasswordField(_('Password'), render_kw={'class':'form-control', 'placeholder': _("Password"), 'required': 'required'})
    confirm_password = PasswordField(_('Confirm Password'), render_kw={'class':'form-control', 'placeholder': _("Confirm Password"), 'required':'required'})

class UserForm(FlaskForm):
    username = TextField(_('Username'), render_kw = {'class':'form-control', 'placeholder': _("Username"), 'required':'required'})
    full_name = TextField(_('Full Name'), render_kw = {'class':'form-control', 'placeholder': _('Full Name'), 'required':'required'})
    password = PasswordField(_('Password'), render_kw={'class':'form-control', 'placeholder': _("Password"), 'required': 'required'})
    confirm_password = PasswordField(_('Confirm Password'), render_kw={'class':'form-control', 'placeholder': _("Confirm Password"), 'required':'required'})
    email = TextField(_('Email'), render_kw={'class':'form-control', 'placeholder': _("Email")})
    is_login_ad = SelectField(
                'Login Type',
                choices=[('Y', _(u'AD')),
                         ('N', _(u'NONE'))], render_kw={'class':'form-control select2'}
            )

class UserTable(Table):
    rowno = RowNumberColumn(_('#'))
    username = Column(_('USERNAME'))
    full_name = Column(_('FULL NAME'))
    email = Column(_('EMAIL'))
    facebook_id = Column(_('FACEBOOK ID'))
    is_login_ad = Column(_('LOGIN WITH AD'))
    create_by = Column(_('CREATE BY'))
    create_at = DateTimeColumn(_('CREATE DATE'))
    action = LamdaColumn('', get_value=lambda row:
                            '<div class="btn-group"> \
                                <a href="%s" class="btn btn-default btn-sm">Edit</a> \
                                <a href="%s" class="btn btn-default btn-sm">Delete</a> \
                             </div>' \
                            % (url_for('admin.UserView:edit', id=row.id),
                               url_for('admin.UserView:delete', id=row.id)
                               ))

class UserView(AdminSecureView):
    """
    UserView
    """

    @route('/index.html', methods=['GET'])
    def index(self):
        table = UserTable(users._search())
        return render_template('/user/index.html', username=users.current_user().username, table=table)

    @route('/add.html', methods=['GET', 'POST'])
    def add(self):
        table = UserTable(users._search())
        form = UserForm()
        error = None

        if form.validate_on_submit():
            user = User()
            user.username = form.username.data.strip()
            user.password = form.password.data
            user.email = form.email.data.strip()
            user.is_login_ad = form.is_login_ad.data.strip()
            user.full_name = form.full_name.data.strip()

            if users.check_duplicate(user.username):
                error = _('Username already exist!')
                return render_template('/user/add.html', username=users.current_user().username, table=table, form=form, error=error)
            if len(user.username) > 50:
                error = _('Username must be less than 50 characters')
                return render_template('/user/add.html', username=users.current_user().username, table=table, form=form, error=error)
            if len(user.full_name) > 50:
                error = _('Full name must be less than 50 characters')
                return render_template('/user/add.html', username=users.current_user().username, table=table, form=form, error=error)

            if form.password.data != form.confirm_password.data:
                error = _('Confirm Password does not match!')
            else:
                users._insert(user)
                return redirect(url_for('admin.UserView:index'))

        return render_template('/user/add.html', username=users.current_user().username, table=table, form=form, error=error)

    @route('/edit.html/<id>', methods=['GET', 'POST'])
    def edit(self, id):
        error = None
        user = users._find(id=id)
        form = UserForm(obj=user)

        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.is_login_ad = form.is_login_ad.data
            user.full_name = form.full_name.data

            if users.check_duplicate(user.username, update=True):
                error = _('Username already exist!')
            else:
                users._update(user)
                return redirect(url_for('admin.UserView:index'))

        return render_template('/user/edit.html', 
                               username=users.current_user().username, 
                               form=form, 
                               error=error,
                               id=id)

    @route('/delete.html/<id>', methods=['GET', 'POST'])
    def delete(self, id):
        user = users._find(id=id)
        form = UserForm(obj=user)

        if form.validate_on_submit():
            users._delete(user)
            return redirect(url_for('admin.UserView:index'))

        return render_template('/user/delete.html', 
                               username=users.current_user().username, 
                               form=form, 
                               id=id)

    @route('/change_password.html/<id>', methods=['GET','POST'])
    def change_password(self, id):
        error = None
        user = users._find(id=id)
        form = ChangePasswordForm()
        form.username.data = user.username

        if user:
            if form.validate_on_submit():
                if form.password.data == form.confirm_password.data:
                    user.password = form.password.data
                    users.change_password(user)
                    return redirect(url_for('admin.UserView:index'))
                else:
                    error = _('Confirm password does not match!')
        return render_template('/user/change_password.html', 
                               form=form, 
                               error=error, 
                               username=users.current_user().username, 
                               id=id)
UserView.register(admin_blueprint)