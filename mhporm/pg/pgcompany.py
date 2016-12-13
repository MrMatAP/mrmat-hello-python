from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from mhporm.pg.pgbase import Base


class PGCompany(Base):
    __tablename__ = 'company'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True)

    people = relationship("PGPerson", back_populates="company")
