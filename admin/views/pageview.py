from admin.views.baseview import *
from flask_babel import lazy_gettext as _
from core.logics.user import users
from core.logics.page import pages, FacebookConfig

class PageTable(Table):
    rowno = RowNumberColumn(_('#'))
    key = Column(_('KEY'))
    value = Column(_('VALUE'))
    #description = Column(_('DESCRIPTION'))
    action = LamdaColumn('', get_value=lambda row:
                            '<div class="btn-group"> \
                                <a href="%s" class="btn btn-default btn-sm">Edit</a> \
                             </div>' \
                            % (url_for('admin.PageView:edit', id=row.id)
                               ))


class PageForm(FlaskForm):
    key = TextField(_('KEY'), render_kw = {'class':'form-control', 'placeholder': _("Key"), 'required':'required', 'oninput':'this.value = this.value.toUpperCase()'})
    value = TextField(_('VALUE'), render_kw = {'class':'form-control', 'placeholder': _("Value"), 'required':'required'})
    description = TextField(_('DESCRIPTION'), render_kw = {'class':'form-control', 'placeholder': _("Description")})

class PageView(AdminSecureView):
    """
    PageView
    """
    @route('/index.html', methods=['GET'])
    def index(self):
        table = PageTable(pages._search())
        return render_template('/page/index.html',
                               username=users.current_user().username,
                               table=table)
    
    @route('/add.html', methods=['GET', 'POST'])
    def add(self):
        form = PageForm()
        error = None

        if form.validate_on_submit():
            obj = FacebookConfig()
            obj.key = form.key.data
            obj.value = form.value.data
            obj.description = form.description.data
            pages._insert(obj)
            return redirect(url_for('admin.PageView:index'))

        return render_template('/page/add.html',
                               username=users.current_user().username,
                               form=form,
                               error=error)

    @route('/edit.html/<id>', methods=['GET', 'POST'])
    def edit(self, id):
        error = None
        config = pages._find(id)
        if config:
            form = PageForm(obj=config)
            if form.validate_on_submit():
                config.key = form.key.data
                config.value = form.value.data
                config.description = form.description.data
                pages._update(config)
                return redirect(url_for('admin.PageView:index'))

        return render_template('/page/edit.html',
                               username=users.current_user().username,
                               form=form,
                               error=error,
                               id=id)

PageView.register(admin_blueprint)