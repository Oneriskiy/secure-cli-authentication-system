import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pathlib import Path
from dotenv import load_dotenv
import base64
from pathlib import Path

load_dotenv()
#paths
users_path = Path(__file__).parent / 'users.txt'

class User_data:
    def __init__(self, username=None, password=None):
        self.__username = username
        self.__password = password

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    def register(self):
        self.__username = input("Введите имя: ")
        self.__password = input("Введите пароль")
        hashing(user.username, user.password)

    def login(self):
        username_login = input("Введите логин: ")
        password_login = input("Введите пароль:")

def hashing(username, password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        salt = salt,
        length = 32,
        iterations = 200_000
    )
    hashed_password = kdf.derive(password.encode())
    base_password = base64.b64encode(hashed_password)
    write_to_file(username, base_password, salt)
    return base_password, salt

def write_to_file(username, base_password, salt):
    with open(users_path, 'a') as file:
        file.write(f'{username}:{base_password.decode()}:{salt}')


def user_menu():
    user_menu_asc = (int
                     (input(
        """Добро пожаловать!
           1 - Вход по логину и паролю
           2 - Регистрация
           >>""".strip())))

    if user_menu_asc == 1:
        user.login()
    elif user_menu_asc == 2:
        print("Окей...давай начнем регистрацию..")
        user.register()

if __name__ == "__main__":
    user = User_data()
    user_menu()