json-py-es
==========
Alexander Liu
* To import raw JSON data files to ElasticSearch using Python

> In the past we import data in this way. Too many jobs by hands...
> ![Alt](static/snapshot106.jpg)
> 
> Using ElasticSearch Bulk API to import this data, sometimes ES only recognizes data in its API way. 
> 
> But now let `json-py-es` glue them all.


jsonpyes
--------
![Alt](static/snapshot104.jpg)

#### Instructions:
    There are 3 proccesses of importing raw JSON data to ElasticSearch
    1. Only validating raw JSON data
    2. Without validating ,just import data to ElasticSearch
    3. After validating successfully, then import data to ElasticSearch


##### 1. Only validating
* ```python jsonpyes.py --data raw_data.json --check```

* If the json data file is valid: 
![Alt](static/snapshot98.jpg)

* If the json data file is invalid: 
![Alt](static/snapshot99.jpg)

##### 2. Only importing without validating
* Notice: If the raw JSON data file is invalid, ElasticSearch will not import it.
* ```python jsonpyes.py --data raw_data.json --bulk http://localhost:9200 --import --index myindex2 --type mytype2```
![Alt](static/snapshot102.jpg)

* And it works.
![Alt](static/snapshot105.jpg)

##### 3. Both validating and importing
* ```python jsonpyes.py --data raw_data.json --bulk http://localhost:9200 --import --index myindex1 --type mytype1 --check```
![Alt](static/snapshot100.jpg)

* And it works.
![Alt](static/snapshot101.jpg)



##### Happy Hacking!
