from __future__ import division
# from pretty import pprint
# import matplotlib.pyplot as plt
from datetime import timedelta, datetime

import json

datetimeformat = "%Y-%m-%d %H:%M:%S.%f" # 2015-12-09 01:18:41.891210

def fiveNumberSummary(lst):
    '''Construct 5 number summary:
    first, min, max, average, last

    Parameters:
        List of Integers
    Returns:
        List of 5 Integers -
            first: First value
            min: Smallest value
            max: Largest value
            avg: The average of all values
            last: Last value
    '''
    assert len(lst) > 0, "list must contain values"

    return {
            "first": lst[0],
            "last": lst[-1],
            "min": min(lst),
            "max": max(lst),
            "avg": sum(lst) / len(lst)
            }

def phaseClassification(correlatedData, time):
    '''Classify each period's phase of flight, and return this list.

    Parameters:
        correlatedData - Data containing details on
                            Timestamps, Altitude, and Speed.
        time - Timestamp of current time being seeked.
    Return:
        str - Phase of Flight described as "Taxi", "Cruise", "Ascend", "Descend",
                or "Unknown".
    '''

    # Set create periods
    period = restructureDataToPeriods(correlatedData, time)

    # Start process
    phases = "Unknown"

    if len(period) == 0:
        return phases
    (timestamps, altitudes, speeds) = zip(*period)

    # plt.plot(altitudes, 'ro')
    # plt.show()

    altitudeSummary = fiveNumberSummary(altitudes)
    speedSummary = fiveNumberSummary(speeds)

    # Check for weird things like if the max is in the middle, and aircraft goes up and back down

    # If there is little altitude difference
    if abs(altitudeSummary["first"] - altitudeSummary["last"]) <= 5:
        #If low speed and low altitude
        if speedSummary["avg"] <= 100 and altitudeSummary["max"] <= 5:
            phases = "Taxi"
        elif abs(altitudeSummary["max"] - altitudeSummary["min"]) <= 5:
            phases = "Cruise"
        else:
            phases = "Unknown"
    else: # Otherwise, large altitude difference
        # Note, this may not be a reliable indicator of whether aircraft is ascending or descending
        if altitudeSummary["first"] < altitudeSummary["last"]:
            phases = "Ascend"
        elif altitudeSummary["first"] > altitudeSummary["last"]:
            phases = "Descend"
        else:
            phases = "Unknown"

    # print altitudeSummary
    # print altitudes

    # print altitudeSummary, speedSummary
    return phases

def ruleClassification(correlatedData, time):
    '''Classifies the rule of flight

    Parameters:
        correlatedData - Data containing details on
                            Timestamps, Altitude, and Speed.
        time - Timestamp of current time being seeked.
    Returns:
        str - Rule of Flight described as "IFR", "VFR", or "Unknown".
    '''

    # Set create periods
    period = restructureDataToPeriods(correlatedData, time)

    # Start process
    rules = "Unknown"

    if len(period) == 0:
        return rules
    elif "flightrules" in period[0]:
        (timestamps, altitudes, speeds, flightrules) = zip(*period)
        actualDataIndex = 0

        for i in range(timestamps):
            if i >= time:
                actualDataIndex = i
                break

        if flightrules[i].find('FR') > -1:
            return flightrules[i]
        elif i > 0 and i < (len(timestamps) - 1) \
                and flightrules[i-1].find('FR') > -1 and flightrules[i+1].find('FR') > -1:
            if abs(altitudes[i] - altitudes[i-1]) <= abs(altitudes[i] - altitudes[i+1]):
                return flightrules[i-1]
            else:
                return flightrules[i+1]
    else:
        (timestamps, altitudes, speeds) = zip(*period)

    altitudeSummary = fiveNumberSummary(altitudes)
    speedSummary = fiveNumberSummary(speeds)

    flightApprox = int(5 * round(float(altitudeSummary["avg"])/5)) % 10

    if flightApprox == 5 or altitudeSummary["avg"] == 0:
        rules = "VFR"
    elif flightApprox == 0:
        rules = "IFR"
    else:
        rules = "Unknown"

    # print int(5 * round(float(altitudeSummary["avg"])/5))
    # print altitudeSummary
    # print altitudes

    return rules

def restructureDataToPeriods(data, time):
    '''Restructure the data so that it consists of data 30 seconds before the
    time given, and 30 seconds after the time given.

    Input python object structure:
    [
        { "timestamp": "2015-12-09 02:42:45.107267", "alt": 87, "speed": 16 },
        { "timestamp": "2015-12-09 02:42:46.101267", "alt": 91, "speed": 21 },
    ]


    Output python object structure:
    [
        1 :
            ("2015-12-09 02:42:45.107267", 87, 16), ("2015-12-09 02:42:46.101267", 91, 21), ...
        2: ...
    ]

    Parameters:
        data - Data containing information on aircraft.
        time - Timestamp of required information
    Returns:
        List of tuples
    '''

    formatTime = datetime.strptime(time, datetimeformat)

    restructured = []

    # For data within time section
    for i in data:
        if i["timestamp"].find('.') <= -1:
            i["timestamp"] += '.000000'
        if (formatTime - timedelta(seconds=30)) <= datetime.strptime(i["timestamp"], datetimeformat) \
            and (formatTime + timedelta(seconds=30)) >= datetime.strptime(i["timestamp"], datetimeformat):
            restructured.append(tuple(i.values()))

    return restructured

def checkData(data):
    ''' Redundancy check integrity of data passed in through JSON

        Remove bad entries by checking for sudden jumps in speed and altitude that do not correlate
        to surrounding entries.

    Parameters:
        data - a set of data points from input
    '''

    # Set threshold to determine unusable entries
    ALT_THRESH = 5          # altitude is in hundred feet
    SPD_THRESH = 100        # speed is in feet/s

    print str(len(data)) + " entries"
    for i in range(len(data)):
        removed = []
        if data[i]["alt"] == 0 and i > 0 and \
                ( (abs(data[i-1]["alt"] - data[i]["alt"]) >= ALT_THRESH) or \
                      abs(data[i]["speed"] - data[i-1]["speed"]) >= SPD_THRESH ):
            print "Removed: " + str(data[i]["alt"]) + ". Entry #" + str(i)
            data.remove(data[i])
