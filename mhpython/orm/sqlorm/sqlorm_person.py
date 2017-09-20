from sqlalchemy import Column, ForeignKey, BigInteger, Integer, String, Date, REAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from mhpython.orm.sqlorm import Base, SQLORMGender, SQLORMBloodType


class SQLORMPerson(Base):
    """
    An ORM person representation

    Note how the id column must be an Integer for SQLite's auto-increment to work
    """
    __tablename__ = "people"

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
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

    gender_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('gender.id'))
    gender_rel = relationship("SQLORMGender", back_populates="people_rel")

    def gender(self, session, name):
        if name is not None:
            existing_gender = session.query(SQLORMGender).filter(SQLORMGender.name.in_(name)).one_or_none()
            if existing_gender is not None:
                self.gender_rel = existing_gender
            else:
                self.gender_rel = SQLORMGender(name)
        elif self.gender_id is not None:
            return self.gender_rel.name
        else:
            return None

    bloodtype_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('bloodtype.id'))
    bloodtype_rel = relationship("SQLORMBloodType", back_populates="people_rel")

    def bloodtype(self, session, name):
        if name is not None:
            existing_bloodtype = session.query(SQLORMBloodType).filter(SQLORMBloodType.name.in_(name)).one_or_none()
            if existing_bloodtype is not None:
                self.bloodtype_rel = existing_bloodtype
            else:
                self.bloodtype_rel = SQLORMBloodType(name)
        elif self.bloodtype_id is not None:
            return self.bloodtype_rel.name
        else:
            return None

    title_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('title.id'))
    title_rel = relationship("SQLORMTitle", back_populates="people_rel")
    title = association_proxy("title_rel", "name")

    cctype_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('cctype.id'))
    cctype = relationship("SQLORMCCType", back_populates="people")

    city_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('city.id'))
    city = relationship("SQLORMCity", back_populates="people")

    company_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('company.id'))
    company = relationship("SQLORMCompany", back_populates="people")

    occupation_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('occupation.id'))
    occupation = relationship("SQLORMOccupation", back_populates="people")

    def __repr__(self):
        return "<SQLPerson(givenname='%s', middleinitial='%s', surname='%s')>" % \
               (self.givenname, self.middleinitial, self.surname)
