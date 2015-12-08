def classifyPhaseOfFlight(periods):
    '''Classifies the phase of flight

    Parameters:
        periods - Contains the altitudes and speeds for each period.
                  List of Dictionary of Lists
    '''
    phases = [None] * len(periods)

    for i in range(len(periods)):
        periods[i]["maxAlt"] = 0
        periods[i]["minAlt"] = 0
        periods[i]["avgAlt"] = 0
        periods[i]["maxSpd"] = 0
        periods[i]["minSpd"] = 0
        periods[i]["avgSpd"] = 0

        #Location of min and max of alt and speed in period i
        altMinLoc = 0
        atMaxLoc = 0
        spdMinLoc = 0
        altMaxLoc = 0

        valid = False
        while not valid:
            altMinLoc = 0
            atMaxLoc = 0
            spdMinLoc = 0
            altMaxLoc = 0
            # for each alt and speed in period
            for j in range(len(periods[i]["alt"])):
                # starting period
                if j == 0:
                    periods[i]["minAlt"] = periods[i]["alt"][j]
                    periods[i]["minSpd"] = periods[i]["spd"][j]
                    periods[i]["maxAlt"] = periods[i]["alt"][j]
                    periods[i]["maxSpd"] = periods[i]["spd"][j]
                # change minimum altitude
                if periods[i]["minAlt"] > periods[i]["alt"][j]:
                    altMinLoc = j
                    periods[i]["minAlt"] = periods[i]["alt"][j]
                # change maximum altitude
                if periods[i]["maxAlt"] < periods[i]["alt"][j]:
                    altMaxLoc = j
                    periods[i]["maxAlt"] = periods[i]["alt"][j]
                # change minimum speed
                if periods[i]["minSpd"] > periods[i]["spd"][j]:
                    spdMinLoc = j
                    periods[i]["minSpd"] = periods[i]["spd"][j]
                # change maximum speed
                if periods[i]["maxSpd"] < periods[i]["spd"][j]:
                    altMaxLoc = j
                    periods[i]["maxSpd"] = periods[i]["spd"][j]

                # Add averages
                periods[i]["avgAlt"] += periods[i]["alt"][j]
                periods[i]["avgSpd"] += periods[i]["spd"][j]
            # Finish creation of average
            periods[i]["avgAlt"] = periods[i]["avgAlt"] / len(periods[i]["alt"])
            periods[i]["avgSpd"] = periods[i]["avgSpd"] / len(periods[i]["spd"])

        # Check rise or fall of altitude
        altDiff = periods[i]["maxAlt"] - periods[i]["minAlt"]
        if altDiff <= 2:
            # Low altitude change & low speed
            if periods[i]["maxSpd"] <= 10:
                phases[i] = "taxing"
            # Low altitude & high speed
            else:
                phases[i] = "cruising"
        # High altitude change & positive
        elif altMaxLoc > altMinLoc:
            phases[i] = "ascending"
        # High altitude change & negative
        else:
            phases[i] = "descending"
    return phases

def classifyRuleOfFlight(periods):
    '''Classifies the rule of flight

    Parameters:
        periods - Contains the altitudes, speeds, and rule of flight (if any) for each period.
                  Dictionary of Lists (or List of Dictionary of Lists if multiple periods)
    '''
