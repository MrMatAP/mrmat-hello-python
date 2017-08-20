from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from mhpython.orm.sqlorm.sqlorm_base import Base


class SQLORMCountry(Base):
    """
    An ORM country representation

    Note how the id column must be an Integer for SQLite's auto-increment to work
    """
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String)

    cities = relationship("SQLORMCity", back_populates="country")
