json-py-es
==========

[![Build Status](https://travis-ci.org/xros/jsonpyes.svg?branch=master)](https://travis-ci.org/xros/jsonpyes)
[![GitHub release](https://img.shields.io/github/release/xros/jsonpyes.svg)](https://github.com/xros/jsonpyes/releases)
[![PyPI](https://img.shields.io/pypi/dm/jsonpyes.svg)](https://pypi.python.org/pypi/jsonpyes)
[![GitHub license](https://img.shields.io/github/license/xros/jsonpyes.svg)](https://github.com/xros/jsonpyes/blob/master/LICENSE)

Alexander Liu

* To import raw JSON data files to ElasticSearch in one line of commands

### Installation

* ```pip install jsonpyes```  

> In the past we import data in this way. Too many jobs by hands...
> ![before image](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot106.jpg)
> 
> Using ElasticSearch Bulk API to import this data, sometimes ES only recognizes data in its API way. 
> 
> But now let `json-py-es` glue them all.


jsonpyes
--------
* ![user interface](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot236.png)

#### Instructions:
    There are 3 proccesses of importing raw JSON data to ElasticSearch
    1. Only validating raw JSON data
    2. Without validating ,just import data to ElasticSearch
    3. After validating successfully, then import data to ElasticSearch


##### 1. Only validating
* ```jsonpyes --data raw_data.json --check```

* If the json data file is valid: 
![json valid](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot98.jpg)

* If the json data file is invalid: 
![json invalid](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot99.jpg)

##### 2. Only importing without validating
* Notice: If the raw JSON data file is invalid, ElasticSearch will not import it.
* ```jsonpyes --data raw_data.json --bulk http://localhost:9200 --import --index myindex2 --type mytype2```
* Or enable multi-threads ```jsonpyes --data raw_data.json --bulk http://localhost:9200 --import --index myindex2 --type mytype2 --thread 8```
![no threads](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot102.jpg)

* ```jsonpyes``` supports multi-threads when importing data to elasticsearch

* No multi-threads 

    ![benchmarks](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot237.png)

* With 8 threads and `jsonpyes` cuts files into pieces, then destributes to workers fairly 

    ![use helpers.bulk API with multi-threads](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot235.png)

> As you can see these two containers have same docs loaded, if we use **_--thread 8_** it could be several times faster, usually 5 to 10 times faster.
That really depends on your computer/server resources.
This was tested on a 4GB RAM / 2.4Ghz intel i5 Linux x64 laptop system.

* And it works.
![it works](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot105.jpg)

##### 3. Both validating and importing
* ```jsonpyes --data raw_data.json --bulk http://localhost:9200 --import --index myindex1 --type mytype1 --check```
![validating and importing](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot135.png)

* And it works.
![the results](https://raw.githubusercontent.com/xros/jsonpyes/master/static/snapshot101.jpg)



##### Happy hacking!
