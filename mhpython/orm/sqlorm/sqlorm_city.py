from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from mhpython.orm.sqlorm.sqlorm_base import Base


class SQLORMCity(Base):
    """
    An ORM city representation

    Note how the id column must be an Integer for SQLite's auto-increment to work
    """
    __tablename__ = 'city'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    name = Column(String, unique=True)
    state = Column(String)

    country_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('country.id'))
    country = relationship("SQLORMCountry", back_populates="cities")

    people = relationship("SQLORMPerson", back_populates="city")
