from Helpers.httpResponse import HttpResponse
from classes.BaseClass import BaseClass
from Model.User import User as UserModel
from Helpers.password import Password



class User(BaseClass):
    def __init__(self):
        self._additional_methods = {
            'Login': self.login
        }

        super().__init__()

    @staticmethod
    def get_model(new_model: bool = False) -> UserModel:
        return UserModel() if new_model else UserModel

    def login(self, **kwargs):
        data = kwargs.get('data')
        login = data.get('login')
        password = data.get('password')

        if not login:
            return HttpResponse.make(success=False, error_text="Не передан логин")

        if not password:
            return HttpResponse.make(success=False, error_text="Не передан пароль")

        user = self._session.query(self.get_model()).filter(self.get_model().login == login)

        if user and user.count():
            user = user.first()

            if Password.check_hash(user.password, password):
                return HttpResponse.make(data=user.to_dict())

            else:
                return HttpResponse.make(success=False, error_text='не верный пароль')

        else:
            return HttpResponse.make(success=False, error_text='Логин не найден')

