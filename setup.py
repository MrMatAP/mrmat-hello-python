from setuptools import setup, find_packages
from os import path

#
# TODO: Find a way so this actually tests using behave before installing

#
# Build properties

basedir = path.abspath(path.dirname(__file__))

#
# Get the long description from the README

with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mhpython',
    version='1.0.0.dev1',

    #
    # What we build

    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': ['gh-webhook-manager = mhpython.cli:gh_webhook_manager'],
    },

    #
    # Dependencies

    tests_require=[
        'behave',
        'coverage',
        'pyhamcrest'
    ],
    install_requires=[
    ],

    #
    # Metadata for PyPI

    author='Mathieu Imfeld',
    author_email='imfeldma@gmail.com',
    license='MIT',
    description='Small python projects that do not warrant their own repository',
    long_description=long_description,
    url='https://github.com/MrMatAP/mrmat-hello-python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users',
        'Topic :: Picture Catalog',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='utilities'
)
