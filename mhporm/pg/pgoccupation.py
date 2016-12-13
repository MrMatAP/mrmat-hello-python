from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from mhporm.pg.pgbase import Base


class PGOccupation(Base):
    __tablename__ = 'occupation'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True)

    people = relationship("PGPerson", back_populates="occupation")
