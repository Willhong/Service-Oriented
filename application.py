import os
from flask import Flask,render_template, redirect, url_for, request
import logging

from database import base
from database.base import User
from views.menus import menus_blueprint
from views.auth import auth_blueprint, kakao_oauth
from rest_server.resource import TemperatureResource, TemperatureCreationResource, TemperatureByLocationResource
from rest_server.resource_check import resource_blueprint
from flask_restful import Api

from flask_login import LoginManager

application = Flask(__name__)
application.register_blueprint(menus_blueprint, url_prefix='/menus')
application.register_blueprint(auth_blueprint, url_prefix='/auth')
application.register_blueprint(resource_blueprint, url_prefix='/resource')

api = Api(application)
api.add_resource(TemperatureResource, "/resource/<sensor_id>")
api.add_resource(TemperatureCreationResource, "/resource/creation")
api.add_resource(TemperatureByLocationResource, "/resource/location/<location>")


application.config['WTF_CSRF_SECRET_KEY'] = os.urandom(24)
application.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(application)

logging.basicConfig(filename='test.log', level=logging.DEBUG)


@login_manager.user_loader
def load_user(user_id):
    q = base.db_session.query(User).filter(User.id == user_id)
    user = q.first()

    if user is not None:
        user._authenticated = True
    return user


"""
@app.route("/")
def hello():
    print("!!!!!!!!!!!!")
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.error("error")
    logging.critical("critical")
    return "<h1>Hello World!</h1>"
"""
"""

@app.route("/profile/<username>")
def get_profile(username):
    return "profile: " + username


@app.route("/add/<int:var_a>/<int:var_b>")
def get_add(var_a, var_b):
    return "add:" + str((int(var_a) + int(var_b)))


@app.route("/first/<username>")
def get_first(username):
    return "<h3>Hello " + username + "!</h3>"



@app.route('/success/<name>')
def success(name):
   return 'welcome {0}' .format(name)

#return 'welcome %s' % name

"""


@application.route('/')
def hello_html():

    return render_template('index.html', nav_menu="home", kakao_oauth=kakao_oauth)


@application.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['myName']
      return redirect(url_for('success', name=user))
   else:
      user = request.args.get('myName')
      return redirect(url_for('success', name=user))

"""
@app.route('/crawling')
def get_google():
    response = requests.get("http://www.naver.com")
    return response.text"""


@application.errorhandler(404)
def page_not_found(error):
    return "<h1>404 Error</h1>", 404
"""
@app.before_request
def before_request():
    logging.info("before_request")"""


if __name__ == "__main__":
    logging.info("Flask Web Server Started")
    application.debug=True
    application.run(host="0.0.0.0", port="8080")
