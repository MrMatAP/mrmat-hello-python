#!/usr/bin/env python

from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Boolean, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from cassandra.cqlengine import columns, connection
from cassandra.cqlengine.management import drop_keyspace, create_keyspace_simple, drop_table, sync_table
from cassandra.cqlengine.models import Model

#
# Initialize SQLAlchemy for PG

engine = create_engine('postgresql+psycopg2://tweet:tweet@infra.bobeli.org:15432/tweet', echo=True)
Base = declarative_base()

#
# Define the PG Tweet ORM class


class PTweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    tweetid = Column(BigInteger)
    createdat = Column(BigInteger)
    currentuserretweetid = Column(BigInteger)
    favouritecount = Column(Integer)
    inreplytoscreenname = Column(String)
    inreplytostatusid = Column(BigInteger)
    quotedstatusid = Column(BigInteger)
    lang = Column(String)
    retweetcount = Column(Integer)
    source = Column(String)
    content = Column(String)
    isfavourited = Column(Boolean)
    ispossiblysensitive = Column(Boolean)
    isretweet = Column(Boolean)
    isretweeted = Column(Boolean)
    isretweetedbyme = Column(Boolean)
    istruncated = Column(Boolean)
    latitude = Column(REAL)
    longitude = Column(REAL)
    country = Column(String)
    countrycode = Column(String)
    placefullname = Column(String)
    placename = Column(String)
    placetype = Column(String)
    placestreetaddress = Column(String)
    placeurl = Column(String)
    usercreatedat = Column(BigInteger)
    userdescription = Column(String)
    userfavouritescount = Column(Integer)
    userfollowerscount = Column(Integer)
    userfriendscount = Column(Integer)
    userid = Column(BigInteger)
    userlang = Column(String)
    userlistedcount = Column(Integer)
    userlocation = Column(String)
    userminiprofileimageurl = Column(String)
    username = Column(String)
    userscreenname = Column(String)
    usertimezone = Column(String)
    userurl = Column(String)
    userutcoffset = Column(Integer)
    useristranslator = Column(Boolean)
    userisverified = Column(Boolean)

    def __repr__(self):
        return "<Tweet(id='%d', username='%s', content='%s'>" % (self.id, self.username, self.content)


#
# Define the Cassandra Model


class CTweet(Model):
    __table_name__ = 'tweet'
    __keyspace__ = 'tweet'

    id = columns.Integer(primary_key=True)
    tweetid = columns.BigInt(index=True)
    createdat = columns.BigInt(index=True)
    currentuserretweetid = columns.BigInt(index=True)
    favouritecount = columns.Integer(index=True)
    inreplytoscreenname = columns.Text(index=True)
    inreplytostatusid = columns.BigInt(index=True)
    quotedstatusid = columns.BigInt(index=True)
    lang = columns.Text(index=True)
    retweetcount = columns.Integer(index=True)
    source = columns.Text(index=True)
    content = columns.Text(index=True)
    isfavourited = columns.Boolean(index=True)
    ispossiblysensitive = columns.Boolean(index=True)
    isretweet = columns.Boolean(index=True)
    isretweeted = columns.Boolean(index=True)
    isretweetedbyme = columns.Boolean(index=True)
    istruncated = columns.Boolean(index=True)
    latitude = columns.Float(index=True)
    longitude = columns.Float(index=True)
    country = columns.Text(index=True)
    countrycode = columns.Text(index=True)
    placefullname = columns.Text(index=True)
    placename = columns.Text(index=True)
    placetype = columns.Text(index=True)
    placestreetaddress = columns.Text(index=True)
    placeurl = columns.Text(index=True)
    usercreatedat = columns.BigInt(index=True)
    userdescription = columns.Text(index=True)
    userfavouritescount = columns.Integer(index=True)
    userfollowerscount = columns.Integer(index=True)
    userfriendscount = columns.Integer(index=True)
    userid = columns.BigInt(index=True)
    userlang = columns.Text(index=True)
    userlistedcount = columns.Integer(index=True)
    userlocation = columns.Text(index=True)
    userminiprofileimageurl = columns.Text(index=True)
    username = columns.Text(index=True)
    userscreenname = columns.Text(index=True)
    usertimezone = columns.Text(index=True)
    userurl = columns.Text(index=True)
    userutcoffset = columns.Integer(index=True)
    useristranslator = columns.Boolean(index=True)
    userisverified = columns.Boolean(index=True)


class CTweetContent(Model):
    __table_name__ = 'tweetcontent'
    __keyspace__ = 'tweet'

    id = columns.Integer(primary_key=True)
    content = columns.Text(index=True)


#
# Connect to PostgreSQL

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
psess = Session()

#
# Connect to Cassandra

connection.setup(['infra.bobeli.org'], 'tweet', protocol_version=3)
drop_table(CTweet)
sync_table(CTweet)
sync_table(CTweetContent)

#
# Iterate over all tweets to upload them into cassandra

for tweet in psess.query(PTweet).order_by(PTweet.id):
    print("Uploading Tweet: %s" % tweet.id)
    CTweetContent.create(
        id=tweet.id,
        content=tweet.content
    )
    CTweet.create(
        id=tweet.id,
        tweetid=tweet.tweetid,
        createdat=tweet.createdat,
        currentuserretweetid=tweet.currentuserretweetid,
        favouritecount=tweet.favouritecount,
        inreplytoscreenname=tweet.inreplytoscreenname,
        inreplytostatusid=tweet.inreplytostatusid,
        quotedstatusid=tweet.quotedstatusid,
        lang=tweet.lang,
        retweetcount=tweet.retweetcount,
        source=tweet.source,
        content=tweet.content,
        isfavourited=tweet.isfavourited,
        ispossiblysensitive=tweet.ispossiblysensitive,
        isretweet=tweet.isretweet,
        isretweeted=tweet.isretweeted,
        isretweetedbyme=tweet.isretweetedbyme,
        istruncated=tweet.istruncated,
        latitude=tweet.latitude,
        longitude=tweet.longitude,
        country=tweet.country,
        countrycode=tweet.countrycode,
        placefullname=tweet.placefullname,
        placename=tweet.placename,
        placetype=tweet.placetype,
        placestreetaddress=tweet.placestreetaddress,
        placeurl=tweet.placeurl,
        usercreatedat=tweet.usercreatedat,
        userdescription=tweet.userdescription,
        userfavouritescount=tweet.userfavouritescount,
        userfollowerscount=tweet.userfollowerscount,
        userfriendscount=tweet.userfriendscount,
        userid=tweet.userid,
        userlang=tweet.userlang,
        userlistedcount=tweet.userlistedcount,
        userlocation=tweet.userlocation,
        userminiprofileimageurl=tweet.userminiprofileimageurl,
        username=tweet.username,
        userscreenname=tweet.userscreenname,
        usertimezone=tweet.usertimezone,
        userurl=tweet.userurl,
        userutcoffset=tweet.userutcoffset,
        useristranslator=tweet.useristranslator,
        userisverified=tweet.userisverified
    )

#
# Report

print "Uploaded %d CTweets" % CTweet.objects.count()
