from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime
)
from .meta import Base


class Photo(Base):
    __tablename__ = 'photo'
    photo_id = Column(Integer, primary_key=True)
    filename = Column(Text, nullable=False)
    description = Column(Text)
    date_modified = Column(DateTime, nullable=False)
