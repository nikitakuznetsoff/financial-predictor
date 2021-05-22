# from .main import application

from flask import Flask
from flask_cors import CORS


from app.api.news import news_blueprint
from app.api.securities import securities_blueprint
from app.api.users import users_blueprint
from app.api.tasks import tasks_blueprint

application = Flask(__name__)

application.config['secret'] = 'asd'

application.register_blueprint(news_blueprint)
application.register_blueprint(securities_blueprint)
application.register_blueprint(users_blueprint)
application.register_blueprint(tasks_blueprint)

CORS(application)