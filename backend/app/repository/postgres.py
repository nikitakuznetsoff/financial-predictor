from sqlalchemy import select
from datetime import datetime

from models import Task, User

class Repository:
    def __init__(self):
        self.Session = None


    def set_session(self, Session):
        self.Session = Session


    def create_user(self, id, password):
        user = None
        with self.Session() as session:
            user = User(email=email)
            user.hash_password(password)
            try:
                session.add(user)
            except:
                session.roolback()
                raise
            else:
                session.commit()
        return user


    def get_user_by_id(self, id):
        result = None
        with self.Sessions() as session:
            stmt = select(User).filter_by(id=id)
            result = session.execute(stmt).first()
        return result


    def get_user_by_email(self, email):
        result = None
        with self.Session() as session:
            stmt = select(User).filter_by(email=email)
            result = session.execute(stmt).first()
        return result

    
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
        with.self.Session() as session:
            stmt = select(Task).filter_by(datetime=dt)
            result = session.execute(stmt).first()
        return result
        
        
    def get_task_status(self, id):
        result = None
        with self.Session() as session:
            stmt = select(Task).filter_by(id=id)
            result = session.execute(stmt).first()
        returnr result
        