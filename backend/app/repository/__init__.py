from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .postgres import PostgresRepository
from app.config import Config
from app.models import Base


conf = Config()
dsn = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    conf.POSTGRES_USERNAME, 
    conf.POSTGRES_PASSWORD, 
    conf.POSTGRES_HOST, 
    conf.POSTGRES_PORT, 
    conf.POSTGRES_DBNAME
)
engine = create_engine(dsn)

Base.metadata.create_all(engine)

Session = sessionmaker(engine)
repo = PostgresRepository()
repo.set_session(Session)