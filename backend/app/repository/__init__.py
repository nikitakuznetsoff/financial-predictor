from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

from .postgres import PostgresRepository
from .mongo import MongoRepository


from app.config import Config, HerokuConfig
from app.models import Base

conf = Config()
# conf = HerokuConfig()
POSTGRES_DSN = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
    conf.POSTGRES_USERNAME, 
    conf.POSTGRES_PASSWORD, 
    conf.POSTGRES_HOST, 
    conf.POSTGRES_PORT, 
    conf.POSTGRES_DBNAME
)
engine = create_engine(POSTGRES_DSN)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
users_repo = PostgresRepository()
users_repo.set_session(Session)


MONGO_DSN = 'mongodb://{0}:{1}@{2}/{4}'.format(
    conf.MONGO_USERNAME,
    conf.MONGO_PASSWORD,
    conf.MONGO_HOST,
    conf.MONGO_PORT,
    conf.MONGO_DBNAME
)
# MONGO_DSN = 'mongodb+srv://{0}:{1}@cluster0.zi8rm.mongodb.net/finpred?retryWrites=true&w=majority'.format(conf.MONGO_USERNAME, conf.MONGO_PASSWORD)
mongo_client = MongoClient(MONGO_DSN)
securities_repo = MongoRepository()
securities_repo.set_client(mongo_client)



