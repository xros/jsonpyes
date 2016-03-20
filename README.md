json-py-es
==========

[![Build Status](https://travis-ci.org/xros/jsonpyes.svg?branch=master)](https://travis-ci.org/xros/jsonpyes)
[![GitHub release](https://img.shields.io/github/release/xros/jsonpyes.svg)](https://github.com/xros/jsonpyes/releases)
[![PyPI](https://img.shields.io/pypi/dm/jsonpyes.svg)](https://pypi.python.org/jsonpyes)
[![GitHub license](https://img.shields.io/github/license/xros/jsonpyes.svg)](https://github.com/xros/jsonpyes/blob/master/LICENSE)

Alexander Liu

* To import raw JSON data files to ElasticSearch using Python in one line of commands

### Installation

* ```pip install jsonpyes```  

> In the past we import data in this way. Too many jobs by hands...
> ![Alt](static/snapshot106.jpg)
> 
> Using ElasticSearch Bulk API to import this data, sometimes ES only recognizes data in its API way. 
> 
> But now let `json-py-es` glue them all.


jsonpyes
--------
![Alt](static/snapshot139.png)

#### Instructions:
    There are 3 proccesses of importing raw JSON data to ElasticSearch
    1. Only validating raw JSON data
    2. Without validating ,just import data to ElasticSearch
    3. After validating successfully, then import data to ElasticSearch


##### 1. Only validating
* ```jsonpyes --data raw_data.json --check```

* If the json data file is valid: 
![Alt](static/snapshot98.jpg)

* If the json data file is invalid: 
![Alt](static/snapshot99.jpg)

##### 2. Only importing without validating
* Notice: If the raw JSON data file is invalid, ElasticSearch will not import it.
* ```jsonpyes --data raw_data.json --bulk http://localhost:9200 --import --index myindex2 --type mytype2```
* Or enable multi-threads ```jsonpyes --data raw_data.json --bulk http://localhost:9200 --import --index myindex2 --type mytype2 --thread 8```
![Alt](static/snapshot102.jpg)

* ```jsonpyes``` supports multi-threads when importing data to elasticsearch
![Alt](static/snapshot132.png)

> As you can see these two containers have same docs loaded, if we use **_--thread 8_** it could be slightly faster.
That really depends on your computer/server resources.
This was tested on a 4GB RAM / 2.4Ghz intel i5 Linux x64 laptop system.

![Alt](static/snapshot133.png)

* And it works.
![Alt](static/snapshot105.jpg)

##### 3. Both validating and importing
* ```jsonpyes --data raw_data.json --bulk http://localhost:9200 --import --index myindex1 --type mytype1 --check```
![Alt](static/snapshot135.png)

* And it works.
![Alt](static/snapshot101.jpg)



##### Happy hacking!
