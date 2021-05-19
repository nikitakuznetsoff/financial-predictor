from config import Config
from models import Base
from sqlalchemy import create_engine


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
