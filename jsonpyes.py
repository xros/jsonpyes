#!/usr/bin/env python2
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys
import subprocess
import simplejson as json



"""
Instructions:
    There are 3 proccesses of importing raw JSON data to ElasticSearch
    1. Only validating raw JSON data
    2. Without validating ,just import data to ElasticSearch
    3. After validating successfully, then import data to ElasticSearch
"""


def show_version():
        print("1.1.5")


def show_help():
    print("""
               _______ ____  _   __      ______  __      ___________
              / / ___// __ \/ | / /     / __ \ \/ /     / ____/ ___/
         __  / /\__ \/ / / /  |/ /_____/ /_/ /\  /_____/ __/  \__ \\
        / /_/ /___/ / /_/ / /|  /_____/ ____/ / /_____/ /___ ___/ /
        \____//____/\____/_/ |_/     /_/     /_/     /_____//____/
        
                        Import JSON to ElasticSearch using Python
                                                           -- Alexander Liu
            
    This program prints files to standard output.
    Any number of files can be specified.
    Options include:

        --data                  : The JSON data file
        --check                 : Check whether the file is valid raw JSON for ElasticSearch
        --bulk                  : ElasticSearch bulk API address
        --index                 : Index name
        --type                  : Index type
        --import                : Import raw JSON data to ES. This proccess does "--check" and data importing
        --version               : Prints the version number 
        --help                  : Display this help 


    Examples:

    1) Only check
    > $~ python jsonpyes.py --data raw_data.json --check
    > All raw JSON data valid!

    2) Only import without checking
    > $~ python jsonpyes.py --data raw_data.json --bulk http://localhost:9200 --import --index myindex1 --type mytype1
    > Successfully data imported!

    3) Import after checking successfully
    > $~ python jsonpyes.py --data raw_data.json --bulk http://localhost:9200 --import --index myindex1 --type mytype1 --check
    > Successfully data checked and imported!

    """)





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


        data = ""
        bulk = ""
        index = ""
        doc_type = ""
        # Get info from process_jobs
        for job in process_jobs:
            if type(job) == dict:
                if job.has_key('data'):
                    data = job['data']
                if job.has_key('bulk'):
                    bulk = job['bulk']
                if job.has_key('index'):
                    index = job['index']
                if job.has_key('type'):
                    doc_type = job['type']
        # Process the jobs in process_jobs
        # 1) Only check JSON data
        if "check" in process_jobs and "import" not in process_jobs:
            # check JSON
            flag = validate_json_data(json_file=data)
            if flag == True:
                print("All raw JSON data valid!")
            else:
            # if data is not valid, function validate_json_data already dumped error info
                pass
            
            return
        
        # 2) Only import without checking
        elif "check" not in process_jobs and "import" in process_jobs:
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
            
            
        
        # 3) Import after checking successfully
        elif "check" in process_jobs and "import" in process_jobs:
            # check JSON
            flag = validate_json_data(json_file=data)
            if flag == True:
                print("All raw JSON data valid!\n")
            else:
            # if data is not valid, function validate_json_data already dumped error info
                print("JSON data not valid!")
                return
            
            # Begin to import to ElasticSearch
            es = Elasticsearch([bulk], verify_certs=True)
            # read JSON data
            with open(data, 'r') as f:
                for line in f:
                    es.index(index=index, doc_type=doc_type, 
                        #id=2, 
                        body=json.loads(line)
                    )
            
            print("Successfully data checked and imported!")
            return
        
        else:
            show_help()
            return
    
    
        
 
    


if __name__ == "__main__":
    run()
