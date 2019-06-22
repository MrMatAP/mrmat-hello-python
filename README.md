# MrMat :: Hello Python

Small Python projects that don't warrant their own repository

## mhpython

Everything else should migrate here

## mhpython.localization

An example for message l18n in Python. To localize strings, one first has to import gettext, then create a default 
locale for the fallback language, followed by a localization honouring the usual language environment setttings.

Any string that ought to be localized then needs to be wrapped by the special `_(string)` method. You can place
identifiers but then you might just as well leave the standard English text. 

The script then must be passed through `pygettext.py` to produce a `classname.pot`. This extracts the 
strings to be localized. This pot file then needs to be translated into a `languagecode/LC_MESSAGES/classname.po`,
which in turn must be translated into binary via `msgfmt.py`.

What localization is then done at runtime is determined by the usual `LC_` variables but the preferred environment
variable of gettext is actually `LANGUAGE`, which can be set to something like `de_CH:en` to prefer Swiss German if
available but fall back to English when it isn't.

## hackathon-2015

Imports a set of tweets into a Cassandra database, which are then analyzed by Apache Spark.
There's an additional script called tweet-analyze but it currently doesn't work because I
have no idea where I got pyspark-cassandra from anymore.

## py-env

Execution behaviour and environment of the Python interpreter

## py-orm

Exploring ORM using Pythons SQLAlchemy
