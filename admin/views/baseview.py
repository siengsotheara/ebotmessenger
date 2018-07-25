from flask import current_app as app
from flask import render_template, redirect, request, url_for
from flask_classy import FlaskView, route

from flask_wtf import FlaskForm, Form
from wtforms import TextField, PasswordField, HiddenField, validators
from admin.views import admin

from admin.auth import requires_auth


class RestView(FlaskView):
    pass

class RestSecureView(FlaskView):
    #decorators = [requires_auth]
    pass