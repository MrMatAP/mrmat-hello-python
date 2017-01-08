from sqlalchemy import Column, Integer, BigInteger, String, DateTime

from mhp.pictures.base import Base


class PicturePG(Base):
    __tablename__ = 'pictures'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    imageuniqueid = Column(String, nullable=False, unique=True)
    originalpath = Column(String)
    originalname = Column(String)
    datetimeoriginal = Column(DateTime)
    datetimedigitized = Column(DateTime)
    width = Column(Integer)
    height = Column(Integer)

    datetimecreated = Column(DateTime)
    datetimeaccessed = Column(DateTime)
    datetimemodified = Column(DateTime)

    ahash = Column(String)
    phash = Column(String)
    dhash = Column(String)
    whashhaar = Column(String)
    whashdb4 = Column(String)
