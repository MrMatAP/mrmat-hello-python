from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from mhpython.orm.sqlorm.sqlorm_base import Base


class SQLORMTitle(Base):
    """
    An ORM title representation

    Note how the id column must be an Integer for SQLite's auto-increment to work
    """
    __tablename__ = 'titles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    people = relationship("SQLORMPerson", back_populates="title")
