from flask_httpauth import HTTPBasicAuth
from .errors import forbidden, unauthorized
from . import api
from flask import g,jsonify
from ..models import User
from .. import login_manager
auth = HTTPBasicAuth()

@auth.verify_password
def verify__password(email_or_token, password):
    if email_or_token == '':
        g.current_user = login_manager.anonymous_user
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('失败')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('未认证的账户')

@api.route('/token')
def get_token():
    if g.current_user.is_anonymous and g.token_used: #申请令牌，匿名用户或者申请过令牌的g.token_used为True的不能再申请
        return unauthorized('失败')
    return jsonify({'token':str(g.current_user.generate_auth_token(expiration=3600)), 'expiration':3600})
