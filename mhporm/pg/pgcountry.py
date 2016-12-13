from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from mhporm.pg.pgbase import Base


class PGCountry(Base):
    __tablename__ = 'country'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String)

    cities = relationship("PGCity", back_populates="country")
