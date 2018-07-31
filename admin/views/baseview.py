from flask_babel import lazy_gettext as _
from flask import current_app as app
from flask import render_template, redirect, request, url_for, make_response
from flask_classy import FlaskView, route
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField, validators


from admin import admin_blueprint
from admin.auth import requires_auth

from common.flask_helpers import *
from common.json_helpers import *
from common.ui.dynamicselect import DynamicSelectField
from common.ui.table import Table, Column, CheckColumn, RowNumberColumn, LamdaColumn, DateColumn, DateTimeColumn, DecimalColumn
from common.ui.dataview import DataView

import requests

class AdminView(FlaskView):
    pass

class AdminSecureView(FlaskView):
    decorators = [requires_auth]
    #pass