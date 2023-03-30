from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text
)
from .meta import Base


class Page(Base):
    __tablename__ = 'page'
    page_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text)
    key = Column(Text, nullable=False)
    menu_order = Column(Integer)


Index('page_un', Page.key, unique=True, mysql_length=48)
