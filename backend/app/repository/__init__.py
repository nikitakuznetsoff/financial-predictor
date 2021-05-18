from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import motor.motor_asyncio
from pymongo import MongoClient

from .postgres import PostgresRepository
from .mongo import MongoRepository
from app.config import Config
from app.models import Base


conf = Config()
POSTGRES_DSN = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
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


MONGO_DSN = 'mongodb://{0}:{1}@{2}/{3}'.format(
    conf.MONGO_USERNAME,
    conf.MONGO_PASSWORD,
    conf.MONGO_HOST,
    conf.MONGO_DBNAME
)
mongo_client = MongoClient(MONGO_DSN)
# mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DSN)
securities_repo = MongoRepository()
securities_repo.set_client(mongo_client)



