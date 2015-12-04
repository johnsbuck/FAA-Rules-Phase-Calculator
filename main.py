# Usage: python main.py test.json

import sys
import json
from pprint import pprint

import classifier

filename = sys.argv[1]

def importJSONFile():
	"""Imports data from file specified in commandline argument 1"""
	data = json.load(file(filename))
	# pprint(data)
	return data

def callModule(data):
	"""Calls module file"""
	classifier.classify(data)


callModule(importJSONFile())
