from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user


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

        # Retorna: user, error_message

        return user, None
    
    @staticmethod
    def login(username, password):
        user = UserRepository.get_by_username(username)

        if not user:
            return None, "Usuario no encontrado"

        valid_password = check_password_hash(user.hashed_password, password)

        if not valid_password:
            return None, "Contraseña incorrecta"
        
        # Retorna: user, error_message

        return user, None