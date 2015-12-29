from distutils.core import setup 
from jsonpyes import version


from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()


setup(name='jsonpyes',
        version=version,
        author="Alexander Liu",
        license="GPL V3",
        description="Import JSON raw data to ElasticSearch using Python in one line of commands",
        long_description=long_description,
        platforms=["Unix","Linux","OSX","Android","Windows"],
        url="https://github.com/xros/jsonpyes",
        download_url="https://github.com/xros/jsonpyes/tarball/" + version,
        #py_modules=['elasticsearch','jsonpyes','simplejson'],
        install_requires=[
            'elasticsearch',
            'simplejson',
        ],
        keywords=["elasticsearch","json","json2es","jsonpyes"],
        classifiers=[],
        # Make this script executable in command line
        scripts=['jsonpyes.py'],
        packages=['contrib', ],
        )
