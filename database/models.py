from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text
from database.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    viora_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)