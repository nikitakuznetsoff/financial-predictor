from flask import Flask
from flask_cors import CORS

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Config
from app.repository import PostgresRepository
from app.news import bp as news_blueprint
# from .auth import bp as auth_blueprint
from app.securities import bp as security_blueprint

conf = Config()
dsn = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    conf.POSTGRES_USERNAME, 
    conf.POSTGRES_PASSWORD, 
    conf.POSTGRES_HOST, 
    conf.POSTGRES_PORT, 
    conf.POSTGRES_DBNAME
)
engine = create_engine(dsn)
Session = sessionmaker(engine)
repo = PostgresRepository()
repo.set_session(Session)

application = Flask(__name__)
application.register_blueprint(news_blueprint)
# application.register_blueprint(auth_blueprint)
application.register_blueprint(security_blueprint)

CORS(application)