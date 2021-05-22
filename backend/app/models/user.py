from sqlalchemy import Column, String, Integer, DateTime, ARRAY
from passlib.hash import pbkdf2_sha256
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from datetime import datetime

from app.config import Config
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    registration = Column(DateTime)
    subscriptions = Column(ARRAY(String))
    

    def hash_password(self, password):
        self.password = pbkdf2_sha256.encrypt(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def get_dict_repr(self):
        d = {
            'id': self.id,
            'email': self.email,
            'registration': self.registration.strftime("%Y-%m-%d %H:%M:%S"),
            'subscriptions': self.subscriptions,
            'username': self.username
        }
        return d

    def generate_auth_token(self, expiration=6000):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return data['id']




