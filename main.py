# Usage: python main.py test.json

import json
import os.path
import sys

import module

def importJSONFile(filename):
    '''Imports data from file specified in commandline argument 1
    '''
    data = json.load(file(filename))
    # pprint(data)
    return data

def callModule(data):
    '''Calls module file

    Parameters:
        data - Dictionary containing other parameters
    '''
    module.classifyPhaseOfFlight(data)

# START OF SCRIPT
if len(sys.argv) >= 2:
    if os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.json'):
        callModule(importJSONFile(sys.argv[1]))
