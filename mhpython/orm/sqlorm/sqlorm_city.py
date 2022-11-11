from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from mhpython.orm.sqlorm.sqlorm_base import Base
from .sqlorm_country import SQLORMCountry


class SQLORMCity(Base):
    """
    An ORM city representation

    Note how the id column must be an Integer for SQLite's auto-increment to work
    """
    __tablename__ = 'city'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    name = Column(String, unique=True)
    state = Column(String)

    people = relationship("SQLORMPerson", back_populates="city_rel")

    country_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('country.id'))
    country_rel = relationship("SQLORMCountry", back_populates="cities_rel")

    def country(self, session, name, code):
        if name is None:
            return None if self.country_rel is None else self.country_rel.name
        try:
            self.country_rel = session.query(SQLORMCountry).filter(SQLORMCountry.name.is_(name)).one()
        except NoResultFound:
            self.country_rel = SQLORMCountry(name, code)

    def __init__(self, session, name, state, country, code):
        self.name = name
        self.state = state
        try:
            self.country_rel = session.query(SQLORMCountry).filter(SQLORMCountry.name.is_(country)).one()
        except NoResultFound:
            self.country_rel = SQLORMCountry(country, code)
