import datetime
from typing import List

from sqlalchemy import Column, Integer, DateTime

from app import Model, engine
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class BaseModel(Model):
    __abstract__ = True
    session = engine.session

    _guarder: List[str] = []
    _fillable: List[str] = []
    _manual_fillable: List[str] = []

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    def from_object(self, record: dict, create_method: bool = False):
        """
        Cоздание модели из словаря
        :param record: Запись словаря с данными
        :return:
        """
        fields = self._get_fillable_fields()

        for field in fields:
            if field.key in record:
                setattr(self, field.key, record.get(field.key))

        if not self.created_at:
            self.created_at = datetime.datetime.now()
        else:
            self.updated_at = datetime.datetime.now()

        if not create_method:
            self._manual_fillable_field(record)

        return self

    def to_dict(self) -> dict:
            """
            преобразование модели в словарь
            :param self:
            :return: Словарь данными из модели
            """

            result = {}

            columns = self._get_columns()

            for column_name in columns:
                result[column_name.key] = getattr(self, column_name.key)

            self._manual_responce_field(result)

            return result

    def add_default_data(self):
        """
        Добавление начальных данных
        """
        pass
    def _manual_fillable_field(self, record: dict):
        """
        Ручное заполнение модели пред сохранением

        """
        pass

    def _manual_responce_field(self, result: dict):
        """
        Заполнение полей перед ответом
        """
        pass

    def _get_columns(self) -> List[str]:
        """
        Получение списка колонок, которые возвращаются из модели
        :return:  Список колонок для метода to_dict
        """
        return self._get_columns_name(self._guarder)

    def _get_fillable_fields(self) -> List[str]:
        """
                получение полей кроме тех которые заполняются вручную
                список полей для авто заполнения в модели
                """

        return self._get_columns_name(self._manual_fillable)

    def _get_columns_name(self, skip_fields: List[str]) -> List[str]:
        columns = self.metadata.tables.get(self.__tablename__).columns
        """
        список полей без учета skip_fields(пропускаемые поля)
        """

        if columns:
            return [column_name for column_name in columns
                    if column_name not in skip_fields]

        return []
