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
    print module.classifyPhaseOfFlight(data)
    # pprint(restructureToPeriods(data))




def restructureToPeriods(data):
    '''Restructure the data so that it consists of one minute intervals
    Input python object structure:
    [
        { "timestamp": "2015-12-09 02:42:45.107267", "alt": 87, "speed": 16 }, 
        { "timestamp": "2015-12-09 02:42:46.101267", "alt": 91, "speed": 21 }, 
    ]


    Output python object structure:
    [
        1 : 
            [
            ("2015-12-09 02:42:45.107267", 87, 16), ("2015-12-09 02:42:46.101267", 91, 21), ...
            ], 
        2: ...
    ]
    '''

    restructured = []
    periodStartTime = datetime.strptime(data[0]["timestamp"], datetimeformat)

    temp = []
    for i in data:
        # When the time difference is greater than one minute,
        # we have our period, and start constructing another
        if  (periodStartTime + timedelta(seconds=60)) < datetime.strptime(i["timestamp"], datetimeformat):
            restructured.append(temp)
            temp = []
            periodStartTime = datetime.strptime(i["timestamp"], datetimeformat)
        # append the datapoint regardless 
        temp.append(tuple(i.values()))

    # Exiting the loop, there may be some left over datapoints.
    if temp:
        restructured.append(temp)

    return restructured

# START OF SCRIPT
if len(sys.argv) >= 2:
    if os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.json'):
        callModule(restructureToPeriods(importJSONFile(sys.argv[1])))
