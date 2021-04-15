from sqlalchemy import Column, String, Integer, Boolean, DateTime

from base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_completed = Column(Boolean)
    datetime = Column(Datetime)