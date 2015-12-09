# Usage: python main.py test.json

import json
import os.path
import sys
from pretty import pprint

import module
from datetime import timedelta, datetime

datetimeformat = "%Y-%m-%d %H:%M:%S.%f" # 2015-12-09 01:18:41.891210

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
    #module.classifyPhaseOfFlight(data)
    #print module.fiveNumberSummary([])
    pprint(restructureToPeriods(data))




def restructureToPeriods(data):
    '''Restructure the data so that it consists of one minute intervals
    Input python object structure:
    [
        {"timestamp": 2000/12/12 12:3456, alt: 300, "speed": 95 },
        {"timestamp": 2000/12/12 12:3458, alt: 300, "speed": 95 },
        {"timestamp": 2000/12/12 12:3702, alt: 300, "speed": 95 },
        {"timestamp": 2000/12/12 12:3704, alt: 300, "speed": 95 },
        ...
    ]

    Output python object structure:
    [
        [
            {"timestamp": 2000/12/12 12:34:56, alt: 300, "speed": 95 },
            {"timestamp": 2000/12/12 12:34:58, alt: 300, "speed": 95 },
            ...
        ],
        [
            {"timestamp": 2000/12/12 12:3702, alt: 300, "speed": 95 },
            {"timestamp": 2000/12/12 12:3704, alt: 300, "speed": 95 },
            ...
        ],
        ...
    ]

    '''
    restructured = []
    periodStartTime = datetime.strptime(data[0]["timestamp"], datetimeformat)
    print periodStartTime

    temp = []
    for i in data:
        # When the time difference is greater than one minute,
        # we have our period, and start constructing another
        if  (periodStartTime + timedelta(seconds=60)) < datetime.strptime(i["timestamp"], datetimeformat):
            restructured.append(temp)
            temp = []
            periodStartTime = datetime.strptime(i["timestamp"], datetimeformat)
        # append the datapoint regardless 
        temp.append(i)

    # Exiting the loop, there may be some left over datapoints.
    if temp:
        restructured.append(temp)

    return restructured

# START OF SCRIPT
if len(sys.argv) >= 2:
    if os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.json'):
        callModule(importJSONFile(sys.argv[1]))
