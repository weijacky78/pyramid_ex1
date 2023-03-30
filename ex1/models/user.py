from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime
)
from .meta import Base


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False)
    email = Column(Text)
    passHash = Column(Text, nullable=False)
    cookieHash = Column(Integer)
    date_modified = Column(DateTime, nullable=False)


Index('user_un', User.username, unique=True, mysql_length=256)
