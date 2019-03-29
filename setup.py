#!/usr/bin/env python2
from distutils.core import setup 
from setuptools import find_packages

import codecs

# Try to build doc, converting from language markdown to rst using pandoc if it is installed
import re
import platform
import subprocess
import os
import sys

CUR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))


# py_version = platform.python_version_tuple()

convert_the_doc_command = "pandoc --from=markdown --to=rst --output=" + os.path.join(CUR_DIR_PATH, "README.rst") + " " + os.path.join(CUR_DIR_PATH, "README.md")


# Trying to build the doc
try:
    os.popen(convert_the_doc_command)
except Exception as e:
    pass

# subprocess has check_output since python 2.7.0+
# if py_version <= (2, 6, 9):
    # try:
        # result = os.popen(convert_the_doc_command)
    # except Exception, e:
        # pass
# else:
    # try:
        # result = subprocess.check_output(convert_the_doc_command , shell=True)
    # except Exception, e:
        # pass


def read_file(filename, encoding='utf8'):
    """Read unicode from given file."""
    with codecs.open(filename, encoding=encoding) as fd:
        return fd.read()

here = os.path.abspath(os.path.dirname(__file__))

# read version number (and other metadata) from package init
init_fn = os.path.join(here, 'jsonpyes_contrib', '__init__.py')
meta = dict(re.findall(r"""__([a-z]+)__ = '([^']+)""", read_file(init_fn)))

# Get the long description from the README file
readme = read_file(os.path.join(here, 'README.rst'))
readme_md = read_file(os.path.join(here, 'README.md'))
# changes = read_file(os.path.join(here, 'CHANGES.rst'))
version = meta['version']


setup(name='jsonpyes',
        version=version,
        author="Alexander Liu",
        author_email='alex@nervey.com',
        license="FTE V1",
        description="A Tool to Import JSON raw data to ElasticSearch in one line of commands",
        long_description=readme_md,
        long_description_content_type='text/markdown',
        platforms=["Unix","Linux","OSX","Android","Windows"],
        url="https://github.com/xros/jsonpyes",
        # download_url="https://github.com/xros/jsonpyes/tarball/" + version,
        # download_url="https://github.com/xros/jsonpyes/archive/master.zip",
        download_url="https://github.com/xros/jsonpyes/archive/" + version + ".zip",
        #py_modules=['elasticsearch','jsonpyes','simplejson'],
        install_requires=[
            'elasticsearch',
            'simplejson',
        ],
        keywords=["elasticsearch","json","json2es","jsonpyes"],
        classifiers=[],
        # Make this script executable in command line
        #scripts=['jsonpyes.py'],
        scripts=['jsonpyes'],
        #packages=['contrib', ],
        packages=find_packages(),
        include_package_data=True,
)
