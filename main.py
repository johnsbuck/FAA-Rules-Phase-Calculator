# Usage: python main.py test.json

import json
import os.path
import sys

import module

def importJSONFile(filename):
    '''Imports data from file specified in commandline argument 1

    Parameters:
        filename - Name of JSON file to be loaded.
    Returns:
        Python object based on JSON file
    '''
    data = json.load(file(filename))
    # pprint(data)
    return data

def callModule(data, time):
    '''Calls module file and prints the phaseClassification and ruleClassification

    Parameters:
        data - JSON file containing information from aircraft.
    '''

    print module.phaseClassification(importJSONFile(data), time)
    print module.ruleClassification(importJSONFile(data), time)

# START OF SCRIPT
if len(sys.argv) >= 3:
    if os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.json'):
        callModule(sys.argv[1], sys.argv[2])
