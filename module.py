from __future__ import division
# from pretty import pprint
# import matplotlib.pyplot as plt
from datetime import timedelta, datetime

datetimeformat = "%Y-%m-%d %H:%M:%S.%f" # 2015-12-09 01:18:41.891210

def fiveNumberSummary(lst):
    '''Construct 5 number summary:
    first, min, max, average, last
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
            if timestamp >= time:
                actualDataIndex = i
                break

        if flightrules[i].find('FR') > -1:
            return flightrules[i]
        elif i > 0 and i < (len(timestamps) - 1) \
                and flightRules[i-1].find('FR') > -1 and flightRules[i+1].find('FR') > -1:
            if abs(altitudes[i] - altitudes[i-1]) >= abs(altitudes[i] - altitudes[i+1]):
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

    Parameters:
        data - Data containing information on aircraft.
        time - Timestamp of required information
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

    """
    temp = []
    for i in data:
        # When the time difference is greater than one minute,
        # we have our period, and start constructing another
        if  (periodStartTime + timedelta(seconds=60)) < datetime.strptime(i["timestamp"], datetimeformat):
            restructured.append(list(temp))
            temp = []
            periodStartTime = datetime.strptime(i["timestamp"], datetimeformat)
        # append the datapoint regardless
        temp.append(tuple(i.values()))

    # Exiting the loop, there may be some left over datapoints.
    if temp:
        restructured.append(temp)
    """
    return restructured
