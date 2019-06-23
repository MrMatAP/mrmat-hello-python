# MrMat :: Hello Python

Small Python projects that don't warrant their own repository

## mhpython

Everything else should migrate here

## mhpython.localization

An example for message l18n in Python. The process is essentially as follows:

1. Import gettext and enclose strings to be localized within `_("Localized String")'`
2. Extract those strings using either `pygettext.py` or, simpler, by installing Babel into setuptools and then running 
   `python ./setup.py extract_messages`. This produces the `messages.pot` template.
3. Translate `messages.pot` into `locale-code/LC_MESSAGES/message.po`
4. Compile the individual `message.po` files into `message.mo` using either `msgfmt.py` or, simpler, by using
   Babels `python ./setup.py compile_catalog` command
   
Note how there are also `init_catalog` and `update_catalog` commands that remain to be tried.

## hackathon-2015

Imports a set of tweets into a Cassandra database, which are then analyzed by Apache Spark.
There's an additional script called tweet-analyze but it currently doesn't work because I
have no idea where I got pyspark-cassandra from anymore.

## py-env

Execution behaviour and environment of the Python interpreter

## py-orm

Exploring ORM using Pythons SQLAlchemy
