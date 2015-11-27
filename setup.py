from distutils.core import setup 

setup(name='jsonpyes',
        version='1.1.2',
        author="Alexander Liu",
        license="GPL V3",
        description="Import JSON raw data to ElasticSearch using Python in one line of commands",
        platforms=["Unix","Linux","OSX","Android","Windows"],
        url="https://github.com/xros/json-py-es",
        download_url="https://github.com/xros/json-py-es/tarball/1.1.2",
        #py_modules=['elasticsearch','jsonpyes','simplejson'],
        install_requires=[
            'elasticsearch',
            'simplejson',
        ],
        keywords=["elasticsearch","json","json2es","jsonpyes"],
        classifiers=[],
        # Make this script executable in command line
        scripts=['bin/jsonpyes'],
        )
