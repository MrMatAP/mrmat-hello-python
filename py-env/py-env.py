#!env python-3.5

import sys

#
# py-env.py
# Execution behaviour end environment of the Python interpreter


print("Sys:")
for entry in dir(sys):
    print("%s - %s" % (type(entry), entry))
