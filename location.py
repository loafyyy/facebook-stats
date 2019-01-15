#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 13:50:25 2019

@author: jackie
"""

# imports
import json
import os
import datetime
from gmplot import gmplot

# takes in location timestamp in s and converts it to a date
def timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(int(timestamp))
    return date.date()

# open location history json file
directory = os.path.dirname(os.path.realpath(__file__)) + '/location'
filename = 'location_history.json'
filepath = os.path.join(directory, filename)

coordinates = []
dates = []

# get data from json file
with open(filepath) as f:
    location_history = json.load(f)
    locations = location_history['location_history_all']
    for location in locations:
        latitude = location['coordinate']['latitude']
        longitude = location['coordinate']['longitude']
        coordinates.append((latitude, longitude))
        dates.append(timestamp_to_date(location['creation_timestamp']))

# place map at latest coordinate
gmap = gmplot.GoogleMapPlotter(coordinates[0][0], coordinates[0][1], 10)

# place markers
lats, lons = zip(*coordinates)

# plot from earliest to latest date so latest date shows on markers
for i in range(len(coordinates) - 1, -1, -1):
    gmap.marker(lats[i], lons[i], title = str(dates[i]))
             
# draw
gmap.draw("facebook_locations.html")