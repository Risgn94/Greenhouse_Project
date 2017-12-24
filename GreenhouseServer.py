#Library packages
import json
import logging

#Flask Packages
import flask
import flask_login
from flask_httpauth import HTTPBasicAuth
from flask import request, abort, render_template, jsonify, make_response, g

#Flask configuration
app = flask.Flask(__name__)
app.secret_key = 'adnudging4WorldLeader'  # Change this!
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
auth = HTTPBasicAuth()

# Our mock database.
users = {'a': {'password': 'a'}}

API_USER = None

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    try:
        user.is_authenticated = request.form['password'] == users[email]['password']
        return user
    except:
        return False

@app.route('/')
@app.route('/home')
def home():
    return '<h1>AdScripting</h1>' \
           '<p>Hello, and welcome to AdScripting. We are currently working on this project, but at this point, nothing interesting can be found here.</p>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')
    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('overview'))
    return render_template(
        'login.html',
        error_Message="Wrong email or password")

@app.route('/dashboard')
@flask_login.login_required
def overview():
    return render_template(
        'dashboard.html',
        current_user=flask_login.current_user.id
    )

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template(
        'login.html',
        error_Message="You need to login to access this page."
    )

"""
API ROUTES FOR WEBSERVER
"""
@app.route('/api/1.0/moisture', methods=['GET', 'PUT'])
def getMoisture():
    #if request.remote_addr != '127.0.0.1' or request.remote_addr != 'localhost':
    #    return jsonify({'error':'Access Restricted'})
    return jsonify({'data': 'Hello, %s!' % g.user})

@app.route('/api/1.0/moisture/<id>', methods=['GET'])
def getSingleMoisture(id):
    #if request.remote_addr != '127.0.0.1' or request.remote_addr != 'localhost':
    #    return jsonify({'error':'Access Restricted'})
    return jsonify({'data': 'Hello, %s!' % g.user})

@app.route('/api/1.0/temperature', methods=['POST', 'GET'])
def newTemperature():
    pass

@app.route('/api/1.0/temperature/<past>/<to>', methods=['GET'])
def getTemperature(past, to):
    pass

@app.route('/api/1.0/humidity', methods=['POST', 'GET'])
def newHumidity():
    pass

@app.route('/api/1.0/humidity/<past>/<to>', methods=['GET'])
def getHumidity(past, to):
    pass

"""
AUTHORIZATION
"""

@auth.verify_password
def verify_password(username, password):
    if(password == users[username]['password']):
        g.user = users[username]
        return True
    else:
        return False


if(__name__ == '__main__'):
    app.run(
        debug=True,
        port=6789,
        host='0.0.0.0'
    )