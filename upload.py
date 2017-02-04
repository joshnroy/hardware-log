#!hardware-log/bin/python
import csv
from uuid import uuid4
from pymongo import MongoClient

with open('Hardware.csv', 'r') as csvfile:
    mongo = MongoClient('mongodb://josh:password@ds137729.mlab.com:37729/hardware')
    rdr = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in rdr:
        pass
        for x in range(int(row[1])):
            mongo.hardware.hardware.insert_one({'name': row[0],
                'renter-name': '', 'renter-email': '',
                'renter-phone-number': '', 'status': 'available', 'uuid':
                uuid4().hex})
