from sqlalchemy import Column, String

from .base import Base


class Security(Base):
    __tablename__ = "securities"

    id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String)