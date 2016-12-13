from sqlalchemy import Column, ForeignKey, BigInteger, String, Date, REAL
from sqlalchemy.orm import relationship

from mhporm.pg import Base


class PGPerson(Base):
    __tablename__ = "people"

    id = Column(BigInteger, primary_key=True)
    givenname = Column(String)
    middleinitial = Column(String)
    surname = Column(String)
    streetaddress = Column(String)
    zipcode = Column(String)
    emailaddress = Column(String)
    username = Column(String)
    password = Column(String)
    telephonenumber = Column(String)
    maidenname = Column(String)
    birthday = Column(Date)
    ccnumber = Column(String)
    cvv2 = Column(String)
    ccexpires = Column(String)
    nationalid = Column(String)
    upstracking = Column(String)
    vehicle = Column(String)
    domain = Column(String)
    kilograms = Column(String)
    centimeters = Column(String)
    latitude = Column(REAL)
    longitude = Column(REAL)
    guid = Column(String)

    gender_id = Column(BigInteger, ForeignKey('gender.id'))
    gender = relationship("PGGender", back_populates="people")

    bloodtype_id = Column(BigInteger, ForeignKey('bloodtype.id'))
    bloodtype = relationship("PGBloodtype", back_populates="people")

    title_id = Column(BigInteger, ForeignKey('titles.id'))
    title = relationship("PGTitle", back_populates="people")

    cctype_id = Column(BigInteger, ForeignKey('cctype.id'))
    cctype = relationship("PGCCtype", back_populates="people")

    city_id = Column(BigInteger, ForeignKey('city.id'))
    city = relationship("PGCity", back_populates="people")

    company_id = Column(BigInteger, ForeignKey('company.id'))
    company = relationship("PGCompany", back_populates="people")

    occupation_id = Column(BigInteger, ForeignKey('occupation.id'))
    occupation = relationship("PGOccupation", back_populates="people")

    def __repr__(self):
        return "<PGPerson(givenname='%s', middleinitial='%s', surname='%s')>" % \
               (self.givenname, self.middleinitial, self.surname)
