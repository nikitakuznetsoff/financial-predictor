from sqlalchemy import select
from datetime import datetime

from app.models import Task, User

class PostgresRepository:
    def __init__(self):
        self.Session = None


    def set_session(self, Session):
        self.Session = Session


    def create_user(self, email, password):
        user = None
        with self.Session() as session:
            user = User(email=email)
            user.hash_password(password)
            try:
                session.add(user)
            except Exception as e:
                session.roolback()
                raise
            else:
                session.commit()
        return user


    def get_user_by_id(self, id):
        with self.Session() as session:
            user = session.query(User).filter(User.id == id).first()
        return user


    def get_user_by_email(self, email):
        with self.Session() as session:
            user = session.query(User).filter(User.email == email).first()
        return user

    
    def create_task(self):
        dt = datetime.now()
        with self.Session() as session:
            task = Task(is_completed=False, datetime=dt)
            try:
                session.add(task)
            except:
                session.roolback()
            else:
                session.commit()

        result = None
        with self.Session() as session:
            stmt = select(Task).filter_by(datetime=dt)
            result = session.execute(stmt).first()
        return result
        
        
    def get_task_status(self, id):
        result = None
        with self.Session() as session:
            stmt = select(Task).filter_by(id=id)
            result = session.execute(stmt).first()
        return result
        