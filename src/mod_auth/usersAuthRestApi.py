from flask import Blueprint, request
from src import basic_auth
from src import db
from flask import jsonify,g
from models import User
from src import app

auth = Blueprint('auth', __name__, url_prefix='/user')

'''
@auth.route('/', methods=['GET','POST'])
@basic_auth.login_required
def test():
    return "test"
'''

@auth.route('/token', methods = ['POST'])
@basic_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


@auth.route('/addUser', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        app.render_error(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        app.render_error(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201


@basic_auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True