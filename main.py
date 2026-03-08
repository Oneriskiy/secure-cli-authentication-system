import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv
import base64
from pathlib import Path
import time
import logging as l

# paths
users_path = Path.cwd() / "users.txt"
logs_path = Path.cwd() / "logs"
logs_path.mkdir(exist_ok=True)
logs_file_path = logs_path / "logs.log"

colors = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "PURPLE": "\033[35m",
    "GRAY": "\033[37m",
    "RESET": "\033[0m",
}

load_dotenv()

# logging
logger = l.getLogger(__name__)
logger.setLevel(l.DEBUG)
formatter = l.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console = l.StreamHandler()
handler = l.FileHandler(filename=str(logs_file_path))
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)


class User_data:
    """
    Класс инициализирует логин и пароль, имеет декораторы для удобного использования атрибутов
    Атрибуты:
    username (str): логин пользователя
    password (str): пароль пользователя
    """

    def __init__(self, username=None, password=None):
        self.__username = username
        self.__password = password

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password


class User_login(User_data):
    """
    Класс, наследник User_data, принимает регистрацию пользователя и вход в аккаунт
    Методы:
    register(): регистрирует логин и пароль пользователя, для дальнейшей записи в файл
    login(): принимает логин и пароль для сверки и подтверждения входа
    check_password(): метод проверяет логин и пароль
    """

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
        user_hashing = User_hashing(self.__username, self.__password)
        user_hashing.hashing(self.__password)

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
        if self.check_password(username_login, password_login):
            print(f"{colors.get('GREEN')}Вход успешен!{colors.get('RESET')}")
        else:
            print(f"{colors.get('RED')}Неверный логин или пароль{colors.get('RESET')}")

    def check_password(self, username_input, password_input):
        with open(users_path, "r") as file:
            for line in file:
                username, password, salt = line.strip().split(":")
                if username == username_input:
                    unbased_password = base64.b64decode(password)
                    unbased_salt = base64.b64decode(salt)
                    break
            else:
                print("Пользователь не найден")
                return False
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=unbased_salt,
                iterations=200_000,
            )
            try:
                kdf.verify(password_input.encode(), unbased_password)
                return True
            except Exception:
                return False


class User_hashing(User_data):
    """
    Класс, наследник User_data, хеширует пароль пользователя и заносит в файл
    Методы:
    hashing(): Хэширует пароль
    write_to_file(): Записывает Логин, Хэш и Соль в файл users_txt
    """

    def hashing(self, password):
        salt = os.urandom(16)
        logger.info("\nначало хеширования")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), salt=salt, length=32, iterations=200_000
        )
        hashed_password = kdf.derive(password.encode())
        base_password = base64.b64encode(hashed_password)
        base_salt = base64.b64encode(salt)
        self.write_to_file(self.username, base_password, base_salt)
        logger.debug("\nпароль хеширован")

    def write_to_file(self, username, base_password, base_salt):
        with open(users_path, "a") as file:
            file.write(f"{username}:{base_password.decode()}:{base_salt.decode()}\n")
            logger.debug("\nЛОГИН:ХЭШ:СОЛЬ - записаны в файл")


def decoration_loading():
    for _ in range(1, 10):
        print(f"{colors.get('RED')}||{colors.get('RESET')}", end="")
        time.sleep(0.1)


def user_menu():
    while True:
        try:
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
                user_login.login()
            elif user_menu_asc == 2:
                logger.debug("\nВыбрана регистрация")
                print("Окей...давай начнем регистрацию..")
                user_login.register()
            else:
                print(
                    f"\n{colors.get('GRAY')}Вы ввели некорректное число{colors.get('RESET')}"
                )
            time.sleep(0.5)
        except ValueError:
            print(f"\n{colors.get('GRAY')}Введите число{colors.get('RESET')}")
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nДо скорой встречи")
            break


if __name__ == "__main__":
    user = User_data()
    user_login = User_login()
    user_menu()
