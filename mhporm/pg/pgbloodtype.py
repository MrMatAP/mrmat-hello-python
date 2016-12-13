from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from mhporm.pg.pgbase import Base


class PGBloodtype(Base):
    __tablename__ = 'bloodtype'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True)

    people = relationship("PGPerson", back_populates="bloodtype")
