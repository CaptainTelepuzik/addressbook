import hashlib
import uuid


class Password:
    """
    Класс для работы с паролями и хэшами
    """
    def __init__(self):
        self._salt = uuid.uuid4().hex

    def get_hash(self, password: str):
        """
        Метод создания хэша пароля
        :param password: пароль
        :return: Захешированный пароль с солью
        """
        return hashlib.sha256(self._salt.encode() + password.encode()).hexdigest() + ':' + self._salt

    @staticmethod
    def check_hash(hashed_password: str, user_password: str) -> bool:
        """
        Проверка хэшированного пароля и переданного
        :param hashed_password: Захешированный пароль
        :param user_password: Пароль пользователя
        :return: Результат сравнения
        """
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

