from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from mhporm.pg.pgbase import Base


class PGGender(Base):
    __tablename__ = 'gender'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True)

    people = relationship("PGPerson", back_populates="gender")
