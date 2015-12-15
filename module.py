from __future__ import division
from pretty import pprint
import matplotlib.pyplot as plt

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
    periods = restructureDataToPeriods(correlatedData, time)

    # Start process
    phases = []

    for period in periods:
        
        (timestamps, altitudes, speeds) = zip(*period)

        plt.plot(altitudes, 'ro')
        plt.show()

        altitude_summary = fiveNumberSummary(altitudes)
        speed_summary = fiveNumberSummary(speeds)

        # Check for weird things like if the max is in the middle, and aircraft goes up and back down

        # If there is little altitude difference
        if abs(altitude_summary["max"] - altitude_summary["min"]) < 5:
            #If low speed and low altitude
            if speed_summary["avg"] <= 10 and altitude_summary["max"] <= 5: 
                phases.append("Taxi")
            # High altitude
            else if altitude_summary["max"] > 5: 
                phases.append("Cruise")
            else:
                phases.append("Unknown")
        else: # Otherwise, large altitude difference
            # Note, this may not be a reliable indicator of whether aircraft is ascending or descending
            if altitude_summary["first"] < altitude_summary["last"]:
                phases.append("Ascend")
            else if altitude_summary["first"] > altitude_summary["last"]:
                phases.append("Descend")
            else:
                phases.append("Unknown")

        # print altitude_summary, speed_summary

    return phases

def ruleClassification(correlatedData, time):
    '''Classifies the rule of flight

    Parameters:
        correlatedData - Data containing details on
                            Timestamps, Altitude, and Speed.
        time - Timestamp of current time being seeked.
    '''

    # Set create periods
    periods = restructureDataToPeriods(correlatedData, time)

    # Start process
    rules = []
    
    for period in periods:
        (timestamps, altitudes, speeds, flightrules) = zip(*period)

        plt.plot(altitudes, 'ro')
        plt.show()
        
        

def restructureToPeriods(data, time):
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
