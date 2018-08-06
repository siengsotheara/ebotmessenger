from admin.views.baseview import *
from flask_babel import lazy_gettext as _
from core.logics.user import users

class UserForm(FlaskForm):
    username = TextField(_('Username'), render_kw = {'class':'form-control', 'placeholder': _("Username"), 'required':'required'})
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
        return render_template('/user/add.html', username=users.current_user().username, table=table, form=form)

    @route('/edit.html/<id>', methods=['POST'])
    def edit(self, id):
        pass

    @route('/delete.html/<id>')
    def delete(self, id):
        pass

    @route('/changepassword.html/<id>', methods=['POST'])
    def change_password(self, id):
        pass
UserView.register(admin_blueprint)