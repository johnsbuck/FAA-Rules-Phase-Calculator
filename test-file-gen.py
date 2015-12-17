#! /usr/bin/python

# The format generated is:
#
# [
#     {"timestamp": 2000/12/12 123456, alt: 300, "speed": 95 },
#     {"timestamp": 2000/12/12 123556, alt: 300, "speed": 95 }
# ]


import json
import random
from datetime import date, time, datetime, timedelta
# from pretty import pprint


# Global variables
timestamp = datetime.now()
alt = int(random.random() * 500)
speed = int(random.random() * 50)
data = []


def randomTimeDelta(minmilli=200, maxmilli=1000):
    ''' Return a time increment '''
    milli = int(round(random.random() * (maxmilli-minmilli))) + minmilli
    return timedelta(milliseconds=milli)

def randomDelta(maxdelta=5):
    return int(round(random.random() * maxdelta)) * random.choice([-1, 0, 1])

def createDatapoint(timestamp, alt, speed):
    ''' Return a tuple (timestamp, alt, speed) '''
    return (timestamp + randomTimeDelta(), alt + randomDelta(), speed + randomDelta())


for i in range(100000):
    (timestamp, alt, speed) = createDatapoint(timestamp, alt, speed)
    data.append({"timestamp": str(timestamp), "alt": alt, "speed": speed})

print json.dumps(data, indent=4)
