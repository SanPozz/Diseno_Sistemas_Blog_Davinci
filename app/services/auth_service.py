from werkzeug.security import generate_password_hash

from app.models.Users import User
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def register(username, email, password):

        existing_email = UserRepository.get_by_email(email)

        if existing_email:
            return None, "Email ya registrado"

        existing_username = UserRepository.get_by_username(username)

        if existing_username:
            return None, "Username ya existe"

        hashed_password = generate_password_hash(password)

        user = User(username=username, email=email, hashed_password=hashed_password)

        UserRepository.create(user)

        return user, None
