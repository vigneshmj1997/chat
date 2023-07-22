from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from user.schemas import User


Base = declarative_base()


class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receiver_id = Column(Integer, ForeignKey(User.id), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    # Define relationships with User table to access sender and receiver details
    sender = relationship(User, foreign_keys=[sender_id])
    receiver = relationship(User, foreign_keys=[receiver_id])