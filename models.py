from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)   
    sender_id = Column(Integer, ForeignKey('users.id'))
    recipient_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)

    sender = relationship('User', foreign_keys=[sender_id])
    recipient = relationship('User', foreign_keys=[recipient_id])
