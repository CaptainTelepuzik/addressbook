from sqlalchemy import Column, Text, DECIMAL, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from Model.BaseModel import BaseModel

class Contact(BaseModel):
    __tablename__ = 'contacts'

    user_id = Column(Integer, ForeignKey('users.id'))
    contact_name = Column(Text, nullable=False)
    contact_surname = Column(Text)
    telephone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)

    user = relationship('User', foreign_keys=[user_id])