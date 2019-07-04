#!/usr/bin/env python2
# encoding: utf-8
"""
                          __________________
                         / ____/_  __/ ____/
                        / /_    / / / __/
                       / __/   / / / /___
                      /_/     /_/ /_____/

                   FREER THAN EVER PUBLIC LICENSE

                        Version 1, March 2016

             Copyright (C) 2016 Alexander Liu <alex(at)nervey.com>

If there exists a most free license, this will be freer than it.
Everyone is permitted to copy, distribute or modifiy anything under this license.

                   FREER THAN EVER PUBLIC LICENSE
    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

0. You are freer than ever to copy, distribute and modifiy anything under this license.
"""


from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys
import subprocess
import threading
import linecache
import jsonpyes_contrib
from jsonpyes_contrib.utils import count_file_lines as c_file_lines
import logging
import time

try:
    import simplejson as json
except ImportError:
    import json

__author__ = "Alexander Liu"


version = jsonpyes_contrib.__version__


"""
Instructions:
    There are 3 proccesses of importing raw JSON data to ElasticSearch
    1. Only validating raw JSON data
    2. Without validating ,just import data to ElasticSearch
    3. After validating successfully, then import data to ElasticSearch
"""

es = Elasticsearch(['http://localhost:9200'], verify_certs=True)

def show_version():
    print(version)


def show_help():
    print("""
               _______ ____  _   __      ______  __      ___________
              / / ___// __ \/ | / /     / __ \ \/ /     / ____/ ___/
         __  / /\__ \/ / / /  |/ /_____/ /_/ /\  /_____/ __/  \__ \\
        / /_/ /___/ / /_/ / /|  /_____/ ____/ / /_____/ /___ ___/ /
        \____//____/\____/_/ |_/     /_/     /_/     /_____//____/
        
                        Import raw JSON to ElasticSearch in one line of commands
                                                           -- Alexander Liu

                                                           """
                                                           +
                                                           
                                                           version

                                                           +
                                                           """

            
    Options include:

        --data                  : The JSON data file
        --check                 : Check whether the file is valid raw JSON for ElasticSearch
        --bulk                  : ElasticSearch bulk API address
        --index                 : Index name
        --type                  : Index type
        --import                : Import raw JSON data to ES. This proccess does "--check" and data importing
        --thread                : Threads amount, default 1. The more threads, the faster when importing or checking
        --version               : Prints the version number 
        --help                  : Display this help 

    Notice:

        It's recommended that you use multi-threads when importing data. Because it's way faster.


    Examples:

    1) Only check
    > $~ jsonpyes --data raw_data.json --check
    > All raw JSON data valid!

    2) Only import without checking
    > $~ jsonpyes --data raw_data.json --bulk http://localhost:9200 --import --index myindex1 --type mytype1
    > Successfully data imported!

    3) Import after checking successfully with 8 threads
    > $~ jsonpyes --data raw_data.json --bulk http://localhost:9200 --import --index myindex1 --type mytype1 --check --thread 8
    > All raw JSON data valid!
    > Successfully data imported!


    """)

def validate_json_data(json_file=""):
    """
    To validate whether the JSON data file is fully a JSON file without any format invalidation
    """
    if str(json_file)=="":
        raise ValueError("No JSON file was input\n")
    else:
        try:
            f = open(json_file, 'r')
        except IOError as e:
            raise IOError('Can not open the file "%s" with error \n%s\n' % (json_file, str(e)))
        else:
            f.close()
            with open(json_file, 'r') as f:
                for line in f:
                    # try to load each line of JSON data and convert it into Python object
                    try:
                        one_dict = json.loads(line)
                    except Exception as e:
                        print("JSON data not valid with error \n %s \n" % (str(e)))
                        return False
                    else:
                        pass
            # assume all JSON valid
            return True


def worker_import_to_es_for_threading(data='a_raw_file.json', start_line=0, stop_line=0, es=es, index="", doc_type=""):
    # NOTICE: the 'start_line' and 'stop_line' are all included. 'stop_line' can not be omitted.
    actions = []
    try_times = 0
    es = es
    # Using linecache to read big data in RAM
    for i in range(start_line, stop_line + 1):
        # Enhancement: This version of jsonpyes use `elastisearch.helpers.bulk`. Thanks to suggestion from piterjoin
        row = linecache.getline(data, i)
        try:
            action = {
                "_index": index,
                "_type": doc_type,
                "_source": json.loads(row)
            }
        except Exception as e:
            logging.warning(str(e))
            continue

        actions.append(action)

        # https://elasticsearch-py.readthedocs.org/en/master/helpers.html?highlight=helpers#module-elasticsearch.helpers
        # In some cases, the size of 1000 docs can be at around 10 MB. And they are stored in RAM

        if len(actions) >= 5000:
            # try serveral times if ES rejects, is busy or down
            while try_times < 5:
                try:
                    # single chunk_bytes max upto 200 MB assumption
                    helpers.bulk(es, actions)
                    try_times = 0
                    break
                except Exception as e:
                    try_times = try_times + 1
                    logging.warning("Can not send a group of actions(docs) to ElasticSearch using parallel_bulk, with error: " + str(e))
                    # wait for the ElasticSearch to response
                    time.sleep(5)
            if try_times >= 5:
                msg = "After trying " + str(try_times) + \
                    " times. It still can not send a group of actions(docs) to ElasticSearch using parallel_bulk, with error: " + str(e)
                logging.error(msg)
                try_times = 0

            # delete previous docs
            del actions[0:len(actions)]

    # clear all the caches out of the for-loop every time -- loop
    linecache.clearcache()

    # if we have leftovers, finish them
    if len(actions) > 0:
        try:
            helpers.bulk(es, actions)
        except Exception as e:
            logging.warning("Can not send a group of actions(docs) to ElasticSearch using parallel_bulk, with error: " + str(e))
        # delete previous docs
        del actions[0:len(actions)]

    # terminate this job
    return

def new_return_start_stop_for_multi_thread_in_list(lines=0, thread_amount=1):
    """Return a list
    Return lines to read for each thread equally
    for example. 37 lines, 4 threads

    [
        {"start": 1, "stop": 10},
        {"start": 11, "stop": 20},
        {"start": 21, "stop": 30},
        {"start": 31, "stop": 37}
    ]

    # start from line 1, ends at line 37 (includes line 37 in data file)

    """


    # lets assume if there were 17 lines and 4 threads, 
    # thread (1)(2)(3) can have 5 job tasks maximumly. thread (4) only has 2 job tasks
    #
    # their job list:
    #               iter 0        iter 1             iter 2            iter 3
    #               thread 1      thread 2           thread 3          thread 4
    # line/job num  1,2,3,4,5     6,7,8,9,10         11,12,13,14,15    16,17
    #
    # iter means iteration
    #

    start_stop_line_list = []
    each_has = lines / thread_amount 
    # last_remains = lines - (thread_amount * each_has)
    last_remains = lines % thread_amount                        # 17 % 4 -> 1
    
    for t in range(thread_amount):
        start_stop_line_list.append(
            {
                "start": each_has * t + 1,
                "stop": each_has * ( t + 1)
            }
        )
    if last_remains > 0:
        start_stop_line_list[-1] = {
            "start": each_has * (thread_amount - 1) + 1,
            "stop": lines
        }

    return start_stop_line_list





class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()



class Jsonpyes(object):
    """Re-edit this in the future maybe.
    Pending, no need until now
    """
    
    def __init__(self):
        pass

    def count_file_lines(json_files=""):
        return c_file_lines(json_file)

    def validate_json_data(json_file=""):
        """
        To validate whether the JSON data file is fully a JSON file without any format validation
        """
        if str(json_file)=="":
            raise ValueError("No JSON file was input\n")
        else:
            try:
                f = open(json_file, 'r')
            except IOError as e:
                raise IOError('Can not open the file "%s" with error \n%s\n' % (json_file, str(e)))
            else:
                f.close()
                with open(json_file, 'r') as f:
                    for line in f:
                        # try to load each line of JSON data and convert it into Python object
                        try:
                            one_dict = json.loads(line)
                        except Exception as e:
                            print("JSON data not valid with error \n %s \n" % (str(e)))
                            return False
                        else:
                            pass
                # assume all JSON valid
                return True
    
    # TODO add muti-threads support
    def importWithOutChecking(self):
        pass


    def importAfterChecking(self):
        pass


def run():
    """
    """
    
    if len(sys.argv) == 1:
        show_help()
        return
    else:
        # logic set
        process_jobs = []
        
        for i in range(len(sys.argv[0:])):
            if sys.argv[i].startswith("--"):
                try:
                    option = sys.argv[i][2:]
                except:
                    show_help()
                    return

                # show version
                if option == "version":
                    show_version()
                    return

                # show some help
                elif option == "help":
                    show_help()
                    return

                # get the raw data
                elif option == "data":
                    # Add info to jobs
                    process_jobs.append(
                        {"data": sys.argv[i+1]}
                    )

                # get the bulk URL
                elif option == "bulk":
                    # Add info to jobs
                    process_jobs.append(
                        {"bulk": sys.argv[i+1]}
                    ) 
                
                # get the bulk index
                elif option == "index":
                    # Add info to jobs
                    process_jobs.append(
                        {"index": sys.argv[i+1]}
                    ) 
                
                # get the bulk type
                elif option == "type":
                    # Add info to jobs
                    process_jobs.append(
                        {"type": sys.argv[i+1]}
                    ) 
                
                
                # check raw JSON
                elif option == "check":
                    # Add info to jobs
                    process_jobs.append(
                        "check"
                    )

                    
                # check if bulk API is valid      
                elif option == "import":
                    # Add info to jobs
                    process_jobs.append(
                        "import"
                    )

                # add multi-threads support
                elif option == "thread":
                    # Add info to jobs
                    process_jobs.append(
                        {"thread_amount": sys.argv[i+1]}
                    ) 
                    process_jobs.append(
                        "thread"
                    )
                

        data = ""
        bulk = ""
        index = ""
        doc_type = ""
        thread_amount = 1
        # Get info from process_jobs
        # fix the syntax bug after upgrading support from Python2.7 to Python3.6, thanks to @tdracz
        for job in process_jobs:
            if type(job) == dict:
                if 'data' in job:
                    data = job['data']
                if 'bulk' in job:
                    bulk = job['bulk']
                if 'index' in job:
                    index = job['index']
                if 'type' in job:
                    doc_type = job['type']
                if 'thread' in job:
                    thread_amount = int(job['thread_amount'])


        #### 1) Only check not importing
        if ("check" in process_jobs) and ("import" not in process_jobs) :
            # check JSON
            flag = validate_json_data(json_file=data)
            if flag == True:
                print("All raw JSON data valid!")
            return
                
        # Process the jobs in process_jobs
        # 2) Only import without checking
        #### 2.1) import, check , no multi-threads
        if ("check" in process_jobs) and ("import" in process_jobs) and ("thread" not in process_jobs):
            
            # check JSON
            flag = validate_json_data(json_file=data)
            if flag == True:
                print("All raw JSON data valid!")
                
            es = Elasticsearch([bulk], verify_certs=True)
            # read JSON data
            with open(data, 'r') as f:
                for line in f:
                    es.index(index=index, doc_type=doc_type, 
                        #id=2, 
                        body=json.loads(line)
                    )
            
            print("Successfully data imported!")
            return


        #### 2.2) import, no check, no multi-threads
        if ("check" not in process_jobs) and ("import" in process_jobs) and ("thread" not in process_jobs):
            es = Elasticsearch([bulk], verify_certs=True)
            # read JSON data
            with open(data, 'r') as f:
                for line in f:
                    es.index(index=index, doc_type=doc_type, 
                        #id=2, 
                        body=json.loads(line)
                    )
            
            print("Successfully data imported!")
            return


        #### 2.3) import, no check, multi-threads
        if ("import" in process_jobs) and ("check" not in process_jobs) and ("thread" in process_jobs):
   


            # check file lines
            lines = c_file_lines(json_file=data)
            # if lines < 1024, it will only use 1 thread to finish this job, no matter how many you want
            if lines < 1024:
            #if lines < 4:                                              # Only for debugging 
                es = Elasticsearch([bulk], verify_certs=True)
                # read JSON data
                with open(data, 'r') as f:
                    for line in f:
                        es.index(index=index, doc_type=doc_type, 
                            #id=2, 
                            body=json.loads(line)
                        )
            else:
                # calculate each thread reads how many lines
                start_stop_line_list = new_return_start_stop_for_multi_thread_in_list(lines=lines, thread_amount=thread_amount)

                threads = []
                for i in start_stop_line_list:
                    #t = StoppableThread(target=worker_import_to_es_for_threading, args=(data, i['start'], i['stop']))
                    t = threading.Thread(target=worker_import_to_es_for_threading, 
                                         args=(data, i['start'], i['stop'], Elasticsearch([bulk], verify_certs=True), index, doc_type, )
                    )
                    threads.append(t)
                    t.start()
                    t.join()
                    

                # stop all threads if interrupts
                try:
                    while len(threading.enumerate()) > 1:
                        pass
                    print("Successfully data imported!")
                    return
                except KeyboardInterrupt:
                    # for i in threads:
                        # i.stop()
                    print("Data importing interrupted!")
                    exit(0)
                    return

            print("Successfully data imported!")
            return
 
 
         #### 2.4) import, check, multi-threads

        if ("import" in process_jobs) and ("check" in process_jobs) and ("thread" in process_jobs):

            # check JSON
            flag = validate_json_data(json_file=data)
            if flag == True:
                print("All raw JSON data valid!")



            # check file lines
            lines = c_file_lines(json_file=data)
            # if lines < 1024, it will only use 1 thread to finish this job, no matter how many you want
            if lines < 1024:
            #if lines < 4:                                              # Only for debugging 
                es = Elasticsearch([bulk], verify_certs=True)
                # read JSON data
                with open(data, 'r') as f:
                    for line in f:
                        es.index(index=index, doc_type=doc_type, 
                            #id=2, 
                            body=json.loads(line)
                        )
                print("Successfully data imported!")
                exit(0)
                return
            else:
                # calculate each thread reads how many lines
                start_stop_line_list = new_return_start_stop_for_multi_thread_in_list(lines=lines, thread_amount=thread_amount)

                threads = []
                for i in start_stop_line_list:
                    #t = StoppableThread(target=worker_import_to_es_for_threading, args=(data, i['start'], i['stop']))
                    t = threading.Thread(target=worker_import_to_es_for_threading, 
                                         args=(data, i['start'], i['stop'], Elasticsearch([bulk], verify_certs=True), index, doc_type, )
                    )
                    threads.append(t)
                    t.start()
                    t.join()
                    

                # stop all threads if interrupts
                try:
                    # there is at least one main threading for all threadings
                    while len(threading.enumerate()) > 1:
                        pass
                    print("Successfully data imported!")
                    exit(0)
                    return
                except KeyboardInterrupt:
                    print(len(threading.enumerate()))
                    # for i in threads:
                        # i.stop()
                    print("Data importing interrupted!")
                    exit(0)
                    return

 
        else:
            show_help()
            return
    
    
        
 
    


if __name__ == "__main__":
    run()
    exit(0)
