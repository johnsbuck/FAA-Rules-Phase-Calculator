from __future__ import division
from pretty import pprint

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

def classifyPhaseOfFlight(periods):
    '''Classify each period's phase of flight, and return this list.

    Parameters:
        periods - Contains the altitudes and speeds for each period.
                  List of Lists of Dictionaries 
    '''

    phases = []

    for period in periods:
        
        
        (timestamps, altitudes, speeds) = zip(*period)

        altitude_summary = fiveNumberSummary(altitudes)
        speed_summary = fiveNumberSummary(speeds)

        # Check for weird things like if the max is in the middle, and aircraft goes up and back down

        # If there is little altitude difference
        if abs(altitude_summary["max"] - altitude_summary["min"]) < 2:
            #If low speed
            if speed_summary["avg"] <= 10: 
                phases.append("taxing")
            else: 
                phases.append("cruising")
        else: # Otherwise, large altitude difference

            # Note, this may not be a reliable indicator of whether aircraft is ascending or descending
            if altitude_summary["first"] < altitude_summary["last"]:
                phases.append("ascending")
            else:
                phases.append("descending")


        print phases
    return phases

def classifyRuleOfFlight(periods):
    '''Classifies the rule of flight

    Parameters:
        periods - Contains the altitudes, speeds, and rule of flight (if any) for each period.
                  Dictionary of Lists (or List of Dictionary of Lists if multiple periods)
    '''
