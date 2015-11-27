from distutils.core import setup 

setup(name='jsonpyes',
        version='1.0',
        author="Alexander Liu",
        license="GPL V3",
        description="Import JSON raw data to ElasticSearch using Python in one line of commands",
        platforms=["Unix","Linux","OSX","Android","Windows"],
        url="https://github.com/xros/json-py-es",
        download_url="https://pypi.python.org/pypi/jsonpyes",
        py_modules=['elasticsearch','jsonpyes','simplejson']
        )
