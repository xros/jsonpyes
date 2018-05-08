def count_file_lines(json_file=""):
    '''
    # TODO 
    Read lines before using multi-threads to do data importing I/O jobs
    '''

    num_lines = 0
    with open(json_file, 'r') as f:
        for line in f:
            num_lines += 1
    return num_lines

def picklines(thefile, whatlines):
    ''' pick specific lines from a file object 
	    return a list object
    '''
    return [x for i, x in enumerate(thefile) if i in whatlines]


def yieldlines(thefile, whatlines):
    ''' pick specific lines from a file object 
	    return a generator object
    '''
    return (x for i, x in enumerate(thefile) if i in whatlines)
