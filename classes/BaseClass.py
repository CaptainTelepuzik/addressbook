import json

from sqlalchemy import desc
from sqlalchemy.orm import Session

from Helpers.httpResponse import HttpResponse
from Model import BaseModel
from app import engine

class BaseClass:
    USE_NAVIGATION: bool = True
    FIELD_SORT: str = None
    AREA: str = 'BaseClass'

    _session: Session = engine.session
    _additional_methods: dict = None

    def __init__(self):
        self._methods_maps = {
            'Create': self.create,
            'Get': self.get,
            'Delete': self.delete,
            'Update': self.update,
            'List': self.list
        }

        if self._additional_methods:
            self.methods_map.update(self._additional_methods)

    @property
    def methods_map(self):
        """
        Получение доступных методов сущности
        :return: Список методов сущностей
        """
        return self._methods_maps

    @staticmethod
    def get_model(new_model: bool = False) -> BaseModel:
        """
        Получение модели

        :param new_model: Признак создавать экземпляр или нет
        :return: Модель сущности
        """
        return BaseModel() if new_model else BaseModel

    def get(self, **kwargs):
        """
        Получение записи по ключу
        :param kwargs: В date содержится ключ записи
        :return: запись или ошибка
        """
        key = kwargs.get('data')
        query = self._session.query(self.get_model().get(key))

        if query:
            return HttpResponse.make(data=query.to_dict())
        else:
            return HttpResponse.make(success=False, error_text=f"Запись в таблице {self.get_model(True).__tablename__}"
                                                              f"по ключу {key} не найдена")

    def list(self, **kwargs):
        """
        Метод получения списка с фильтрацией

        :param self: Параметры с фильтром
        :param kwargs:
        :return: список записей
        """
        filter_params = kwargs.get('filter')

        result = self._prepare_list_result(filter_params)
        result = self._prepare_list(result, filter_params)

        return HttpResponse.make(data=result)

    def create(self, **kwargs):
        """
        Метод получения формата записи
        :param kwargs: запись с заполнеными полями
        :return: формат записи с предустановленными полями
        """
        model = self.get_model(True)
        record = kwargs.get('data')

        if isinstance(record, str):
            record = json.loads(record)

        if not record:
            data = model.to_dict()
        else:
            data = model.from_object(record, True).to_dict()

        return HttpResponse.make(data=data)

    def update(self, **kwargs):
        """
        Обновление записи или создание записи
        :param kwargs: запись для сохранения
        :return: Обновленная запись
        """
        record = kwargs.get('data')

        if isinstance(record, str):
            record = json.loads(record)

        if not record:
            return HttpResponse.make(success=False, error_text="Не переданные данные")

        if not record.get('id'):
            return self._new(record)
        else:
            return self._update(record)


    def delete(self, **kwargs):
        """
        Удаление записи
        :param kwargs: ключ записи
        :return: результат удаления
        """
        key = kwargs.get('data')
        query = self._session.query(self.get_model()).get(key)

        if query:
            self._session.delete(query)
            self._session.commit()

            return HttpResponse.make()

        else:
            return HttpResponse.make(success=False, error_text="Не найдена запись по ключу")

    def _prepare_list(self, result, filter_params):
        """
        Постобработка перед выдачей результата

        :param result: Список сущностей
        :param filter_params: фильтр
        :return: список обработанных записей
        """
        return result

    def _prepare_list_result(self, filter_params):
        """
        Метод получения результата с фильтрацией

        :param filter_params: Фильтр
        :return: Список записей
        """
        result = []

        query = self._prepare_query_filter(self._session.query(self.get_model()), filter_params)

        if self.FIELD_SORT:
            query.order_by(desc(self.FIELD_SORT))

        count_result = query.count() if query else 0

        if count_result:
            result = [item.to_dict() for item in query.all()]

        return result


    def _prepare_query_filter(self, query, filter_params):
        """
         Применение фильтрации к объекту записи
        :param query: Объект запроса
        :param filter_params: Фильтр
        :return: Объект запроса с фильтрацией
        """
        return query

    def _new(self, record):
        """
        Создание новой записи в БД
        :param record: Данные которые передаем в модель
        :return: Обновленная запись в БД
        """
        model = self.get_model(True)
        model.from_object(record)
        self._session.add_all([model])
        self._session.commit()

        return HttpResponse.make(data=model.to_dict())

    def _update(self, record):
        """
        Обновление записи
        :param record: Обновляемые данные для модели
        :return: Обновленная запись в БД
        """
        model = self._session.query(self.get_model()).get(record.get('id'))

        if model:
            model.from_object(record)
            self._session.add_all([model])
            self._session.commit()

            return HttpResponse.make(data=model.to_dict())
        else:
            return HttpResponse.make(success=False, error_text="Нет записи для обновления БД")











