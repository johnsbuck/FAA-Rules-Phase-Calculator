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
from pretty import pprint

def randomTimeDelta(maxmilli=100):
    """Return a time increment"""
    milli = int(round(random.random() * maxmilli))
    return timedelta(milliseconds=milli)

def randomDelta(maxdelta=5):
    return int(round(random.random() * maxdelta))

def createDatapoint(timestamp=datetime.now(), alt=-100, speed=-100):
    if alt is -100:
        alt = int(random.random() * 500)
    else:
        alt += randomDelta()

    if speed is -100:
        speed = int(random.random() * 50)
    else:
        speed += randomDelta()

    timestamp += randomTimeDelta()

    return {"timestamp": str(timestamp), "alt": alt, "speed": speed}


data = [ createDatapoint() for i in range(1000) ]
print json.dumps(data, indent=4)
