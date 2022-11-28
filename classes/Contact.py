from classes.BaseClass import BaseClass
from Model.Contact import Contact as ContactModel


class Contact(BaseClass):
    @staticmethod
    def get_model(new_model: bool = False) -> ContactModel:
        return ContactModel() if new_model else ContactModel

    def _prepare_query_filter(self, query, filter_params):
        """
         Применение фильтрации к объекту записи
        :param query: Объект запроса
        :param filter_params: Фильтр
        :return: Объект запроса с фильтрацией
        """
        if filter_params.get('X-User_ID'):
            query = query.where(self.get_model().user_id == filter_params.get('X-User_ID'))

        return query
