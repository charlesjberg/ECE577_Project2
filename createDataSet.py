# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 14:29:16 2022

@author: CJ
"""

import csv
import googlemaps
from datetime import datetime
with open('MaTowns.csv', newline='') as csvfile:
        lats = []
        longs = []
        cityNames = []
        Towns = csv.reader(csvfile, delimiter=',')
        for row in Towns:
            cityNames.append(row[0])
            lats.append(row[1])
            longs.append(row[2])
print("Done reading in town names")    
file = open("DistancesToMATowns.txt", "w")
writer = csv.writer(file)
writer.writerow(["From Town Name", "To Town Name", "Distance", "Time"])
APIKEY = "AIzaSyCDQRS5mYEsFAlJFFOdWQpkkDW0XEawJD0"
gmaps = googlemaps.Client(key=APIKEY)
now = datetime.now()
index1 = 0
for towns in cityNames:
    LatLong1 = lats[index1] + "," + longs[index1]
    index1 += 1
    index2 = 0             
#configure api
    for lat in lats:
        now = datetime.now()
        if index2 == (index1-1):
            index2 += 1
        else:
            LatLong2 = lats[index2] + "," + longs[index2] 
            directions_result = gmaps.directions(LatLong1, LatLong2, mode="driving", departure_time=now)
            distance = (directions_result[0]['legs'][0]['distance']['value'])
            duration = (directions_result[0]['legs'][0]['duration']['value'])
            
            print("Distance from " + cityNames[index1-1] + " to " + cityNames[index2] + " is " + (directions_result[0]['legs'][0]['distance']['text']))
            writer.writerow([cityNames[index1-1], cityNames[index2], distance, duration])
            index2 += 1