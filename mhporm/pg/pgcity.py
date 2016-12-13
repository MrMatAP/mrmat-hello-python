from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from mhporm.pg.pgbase import Base


class PGCity(Base):
    __tablename__ = 'city'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True)
    state = Column(String)

    country_id = Column(BigInteger, ForeignKey('country.id'))
    country = relationship("PGCountry", back_populates="cities")

    people = relationship("PGPerson", back_populates="city")
