#!/usr/bin/env python

import sys
from setuptools import setup, find_packages

setup(
    name='mhpython',
    version='0.0.1',
    packages=find_packages(),
    author='Mathieu Imfeld',
    author_email='imfeldma@gmail.com',
    long_description='Small Python projects that do not warrant their own repositories',
    license='BSD 3-Clause',
    keywords=[
        'utilities'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users',
        'Topic :: Picture Catalog',
        'License :: OSI Approved :: BSD',
        'Programming Language :: Python :: 3.7'
    ],

    setup_requires=[
        'wheel>=0.33.4'     # MIT
    ],
    install_requires=[
        'requests>=2.18.1',         # Apache 2.0
        'sqlalchemy>=1.1.13',       # MIT
        'Flask>=1.0.2',             # BSD
        'flask-restplus>=0.11.0',   # BSD
        'flask-pyoidc>=2.0.0',      # Apache 2.0
        'cqlengine>=0.21.0',        # BSD
        'psycopg2>=2.7.4',          # LGPL with exceptions
        'pyspark>=2.3.0',           # Apache 2.0
        'mongoengine>=0.15.0',      # MIT
        'imagehash>=4.0',           # BSD 2-clause
        'piexif>=1.0.13'            # MIT
    ],
    test_requires=[
        'behave>=1.2.5',            # BSD
        'pytest-cov>=2.5.1',        # MIT
        'pytest>=3.2.1',            # MIT
        'sphinx>=1.6.2',            # BSD./se
        'twine>=1.9.1'              # Apache 2.0
    ],

    entry_points={
        'console_scripts': [
            'mrmat-github = mhpython.github.mrmat_github:run',
            'mrmat-oidc-interactive = mhpython.oidc.mrmat_oidc_interactive:run',
            'mrmat-cass-import = mhpython.hackathon_2015.mrmat_cass_import:run',
            'mrmat-tweet-analyze = mhpython.hackathon_2015.mrmat_tweet_analyze:run',
            'mrmat-boilerplate = mhpython.boilerplate.mrmat_boilerplate:run',
            'mrmat-localized = mhpython.localization.localized:run',
            'mrmat-classes = mhpython.classes.mrmat_classes:run',
            'mrmat-env = mhpython.py_env.mrmat_env:run',
            'mrmat-io = mhpython.py_io.mrmat_io:run',
            'mrmat-packages = mhpython.py_packages.mrmat_packages:run',
            'mrmat-spinner = mhpython.py_spinner.mrmat_spinner:run',
            'mrmat-pg-to-mongo = mhpython.orm.mrmat_pg_to_mongo:run'
        ],
    },
    include_package_data=True,
    package_data={
        '': [
            'locale/de/LC_MESSAGES/*.mo',
            'locale/de_CH/LC_MESSAGES/*.mo',
            'locale/en/LC_MESSAGES/*.mo'
        ]
    }

)
