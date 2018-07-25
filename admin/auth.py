from flask import render_template, request, url_for, session, Flask, escape, redirect, Response
from functools import wraps
from app import app , jsonify
from core.logics.base import *


def check_auth(username, password):
    #u = users.authenticate(username, password)
    #if u:
    #    session['user_id']=u.id
    #    session['username']=u.username
    #return u

    return username == BaseConfig.username and password == BaseConfig.password

def authenticate():
    log.info(request.remote_addr + ' '+ request.method+ ' ' + request.url)
    message = {"MESSAGE": "UNAUTHENTICATED","STATUS_CODE":401}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated