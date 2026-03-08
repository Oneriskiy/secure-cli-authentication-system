import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv
import base64
from pathlib import Path
import time
import logging as l

# paths
users_path = Path(__file__).parent / "users.txt"
logs_path = Path(__file__).parent / "logs"
logs_path.mkdir(exist_ok=True)
logs_file_path = logs_path / "logs.log"

colors = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "PURPLE": "\033[35m",
    "RESET": "\033[0m",
}

logger = l.getLogger(__name__)
logger.setLevel(l.DEBUG)
formatter = l.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console = l.StreamHandler()
handler = l.FileHandler(filename=logs_file_path)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)

load_dotenv()


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
        self.__username = input(
            f"{colors.get('PURPLE')}Введите логин: {colors.get('RESET')}"
        )
        logger.debug("\nВведен логин регистрации")
        decoration_loading()
        self.__password = input(
            f"\n{colors.get('BLUE')}Введите пароль: {colors.get('RESET')}"
        )
        logger.debug("\nВведен пароль")
        hashing(user.username, user.password)

    def login(self):
        username_login = input(
            f"{colors.get('PURPLE')}Введите логин: {colors.get('RESET')}"
        )
        logger.debug("\nВведен логин для входа")
        decoration_loading()
        password_login = input(
            f"\n{colors.get('BLUE')}Введите пароль: {colors.get('RESET')}"
        )
        logger.debug("\nВведен пароль")


def decoration_loading():
    for _ in range(1, 10):
        print(f"{colors.get('RED')}||{colors.get('RESET')}", end="")
        time.sleep(0.1)


def hashing(username, password):
    logger.info("\nначало хеширования")
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), salt=salt, length=32, iterations=200_000
    )
    hashed_password = kdf.derive(password.encode())
    base_password = base64.b64encode(hashed_password)
    write_to_file(username, base_password, salt)
    logger.debug("\nпароль хеширован")
    return base_password, salt


def write_to_file(username, base_password, salt):
    with open(users_path, "a") as file:
        file.write(f"{username}:{base_password.decode()}:{salt}\n")
        logger.debug("\nЛОГИН:ХЭШ:СОЛЬ - записаны в файл")


def user_menu():
    user_menu_asc = int(
        input(
            f"""Добро пожаловать!
           1 - {colors.get('PURPLE')}Вход по логину и паролю{colors.get('RESET')}
           2 - Регистрация
           {colors.get('GREEN')}>>{colors.get('RESET')}""".strip()
        )
    )

    if user_menu_asc == 1:
        logger.debug("\nВыбран вход в аккаунт")
        user.login()
    elif user_menu_asc == 2:
        logger.debug("\nВыбрана регистрация")
        print("Окей...давай начнем регистрацию..")
        user.register()


if __name__ == "__main__":
    user = User_data()
    user_menu()
