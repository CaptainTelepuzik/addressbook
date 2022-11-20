from classes.BaseClass import BaseClass
from Model.Contact import Contact as ContactModel


class Contact(BaseClass):
    @staticmethod
    def get_model(new_model: bool = False) -> ContactModel:
        return ContactModel() if new_model else ContactModel

