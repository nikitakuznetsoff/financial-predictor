from flask import Flask
from flask_cors import CORS
from .news import bp as news_blueprint
# from .auth import bp as auth_blueprint
from .security import bp as security_blueprint


application = Flask(__name__)
application.register_blueprint(news_blueprint)
# application.register_blueprint(auth_blueprint)
application.register_blueprint(security_blueprint)

CORS(application)