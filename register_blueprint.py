from runserver import app
from flask import url_for, redirect

from admin import admin_blueprint
app.register_blueprint(admin_blueprint)