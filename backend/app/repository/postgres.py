from sqlalchemy import select, update, delete
from datetime import datetime

from app.models import Task, User


class PostgresRepository:
    def __init__(self):
        self.Session = None

    def set_session(self, Session):
        self.Session = Session

    def create_user(self, email, password, username, reg_date):
        user = None
        with self.Session() as session:
            
            user = User(email=email, username=username, registration=reg_date)
            user.hash_password(password)
            try:
                session.add(user)
            except Exception as e:
                session.roolback()
                raise
            else:
                session.commit()
        return user


    def delete_user(self, user_id):
        with self.Session() as session:
            try:
                session.execute(
                    delete(User)
                    .where(User.id == user_id)
                )
            except:
                session.roolback()
                raise
            else:
                session.commit()

    def get_user_by_id(self, id):
        with self.Session() as session:
            user = session.query(User).filter(User.id == id).first()
        return user

    def get_user_by_email(self, email):
        with self.Session() as session:
            user = session.query(User).filter(User.email == email).first()
        return user

    def add_user_subscription(self, user_id, secid):
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            subs = user.subscriptions
            subs.append(secid)

            session.execute(
                update(User)
                .where(User.id == user.id)
                .values(subscriptions=subs)
            )
            session.commit()
        return user

    def remove_user_subscriptions(self, user_id, secid):
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            subs = user.subscriptions
            subs.remove(secid)
            session.execute(
                update(User)
                .where(User.id == user.id)
                .values(subscriptions=subs)
            )
            session.commit()
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

    def change_username(self, user_id, username):
        user = None
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            user.username = username
            session.commit()
        return user

    def change_email(self, user_id, email):
        user = None
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            user.email = email
            session.commit()
        return user

    def change_password(self, user_id, password):
        user = None
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            user.hash_password(password)
            session.commit()
        return user
