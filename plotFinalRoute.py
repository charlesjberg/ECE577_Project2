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

with open('Results/FinalRoute.csv', newline='') as csvfile:
        routeIndexes = []
        Towns = csv.reader(csvfile, delimiter=',')
        i = 0;
        ALL_Routes = []
        for row in Towns:
            i+=1
            print(i)
            numberofCities = row[2]
            numberofRoutes = row[3]
            if i == int(numberofCities):
                i = 0;
                routeIndexes.append(int(row[1]))
                ALL_Routes.append(routeIndexes)
                routeIndexes = []
            else:
                routeIndexes.append(int(row[1]))

print("Done reading in route")  

APIKEY = "AIzaSyCDQRS5mYEsFAlJFFOdWQpkkDW0XEawJD0"
gmaps = googlemaps.Client(key=APIKEY)
now = datetime.now()
route_LatLonALL = []
for route in ALL_Routes:
    route_LatLon = []
    for indexes in route:
        route_LatLon.append(lats[indexes-1] + "," + longs[indexes-1])
    route_LatLonALL.append(route_LatLon)

i=0;
for latlon in route_LatLonALL:
    results = gmaps.directions(latlon[0],latlon[0], waypoints=latlon[1:-1], mode ="driving",departure_time=datetime.now())
    distance = (results[0]['legs'][0]['distance']['value'])
    duration = (results[0]['legs'][0]['duration']['value'])
    marker_points = []
    waypoints = []         
    for leg in results[0]["legs"]:
        leg_start_loc = leg["start_location"]
        marker_points.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
        for step in leg["steps"]:
            end_loc = step["end_location"]
            waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')
    last_stop = results[0]["legs"][-1]["end_location"]
    marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')
        
    markers = [ "color:blue|size:mid|label:" + chr(65+i) + "|" 
            + r for i, r in enumerate(marker_points)]
    result_map = gmaps.static_map(
                  center = latlon[0],
                  scale=2, 
                  zoom=9,
                  size=[640, 640], 
                  format="jpg", 
                  maptype="roadmap",
                  markers=markers,
                  path="color:0x0000ff|weight:2|" + "|".join(waypoints))
    imageName = "Results/Route" + str(i) + ".jpg"
    print("Creating image " + str(i))
    i+=1
    with open(imageName, "wb") as img:
        for chunk in result_map:
            img.write(chunk)