#!/usr/bin/env python

from setuptools import setup, find_packages

desc = """Machine-readable collection of US and non-US local news media."""

__appversion__ = None

#__appversion__, defined here
exec(open('localnewsrepo/version.py').read())

setup(
    name='localnewsrepo',
    version=__appversion__,
    description=desc,
    long_description='See: https://github.com/anwala/local-news-repo',
    author='Alexander C. Nwala',
    author_email='acnwala@wm.edu',
    url='https://github.com/anwala/local-news-repo',
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_data={
        'localnewsrepo': [
            './sources/usa.json.gz',
            './sources/zipcodes.db',
            './sources/countries_local_media.json.gz'
        ]
    },
    install_requires=[],
    scripts=[
        'bin/lnr'
    ]
)
