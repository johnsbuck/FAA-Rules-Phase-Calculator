# Usage: python main.py test.json

import json
import os.path
import sys

import module

def importJSONFile(filename):
    '''Imports data from file specified in commandline argument 1

    Parameters:
        filename - Name of JSON file to be loaded.
    '''
    data = json.load(file(filename))
    # pprint(data)
    return data

def callModule(data):
    '''Calls module file

    Parameters:
        data - JSON file containing information from aircraft.
    '''

    print "test"
    print module.phaseClassification(importJSONFile(data), "2015-12-16 03:30:41.944000")
    # pprint(restructureToPeriods(data))
    # print module.ruleClassification(importJSONFile(data))

# START OF SCRIPT
if len(sys.argv) >= 2:
    if os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.json'):
        callModule(sys.argv[1])
