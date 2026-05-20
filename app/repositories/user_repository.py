from app.models.Users import User
from app.database import db


class UserRepository:

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()
