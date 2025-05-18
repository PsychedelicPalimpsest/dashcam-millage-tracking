import os, csv
import math, json
import folium
from datetime import datetime
from geopy.geocoders import Nominatim
from datetime import date
import zipfile


from CONFIG import STARTS_AT

PATH = os.path.dirname(os.path.abspath(__file__))
records = os.path.join(PATH, "records")
details = os.path.join(records, "details")

def get_address(lat, lon):
    geolocator = Nominatim(user_agent="dashcam_mileage_tracker")
    location = geolocator.reverse((lat, lon))
    return location.address if location else "Unknown location"


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two GPS coordinates in miles using the Haversine formula.
    
    Args:
        lat1 (float): Latitude of the first point in decimal degrees
        lon1 (float): Longitude of the first point in decimal degrees
        lat2 (float): Latitude of the second point in decimal degrees
        lon2 (float): Longitude of the second point in decimal degrees
    
    Returns:
        float: Distance between the points in miles
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in miles
    r = 3956
    
    # Calculate distance
    distance = c * r
    
    return distance





PATH = os.path.dirname(os.path.abspath(__file__))


jsonOut = os.path.join(PATH, "json")





def main():
    miles = 0
    last_long, lost_lat = None, None
    gps_data = []
    path = []

    new_file_markers = []
    start_at = STARTS_AT
    
    start_time = None
    end_time = None

    start_location = None
    end_location = None


    for j in sorted(os.listdir(jsonOut)):
        f = open(os.path.join(jsonOut, j), "r")
        results = json.loads(f.read())
        f.close()

        if start_at is not None and start_at != j:
            continue
        start_at = None
        new_file = True

        for r in results:
            if len(r["location"]) != 3:
                continue
            try:
                _, lat, lon = r["location"]
                lat, lon = float(lat), float(lon)
            except ValueError:
                # print("Invalid location", r["location"])
                continue
            
            if abs(lat - 40) > 0.6:
                # print("INVALID LAT:", (lat, lon))
                continue
            if abs(lon - 83) > 0.6:
                # print("INVALID LONG:", (lat, lon))
                continue

            lon = -lon


            if start_location is None:
                start_location = (lat, lon)
            end_location = (lat, lon)

            if start_time is None and len(r["date"].split(":")) == 3:
                start_time = r["date"] # TODO: Change to time
            if len(r["date"].split(":")) == 3:
                end_time = r["date"] # TODO: Dito


                gps_data.append([r["date"], lat, lon])

            if new_file:
                new_file = False
                new_file_markers.append(folium.Marker(location=(lat, lon), popup=f"File: {j}", icon=folium.Icon(color="green")))
            path.append((lat, lon))


            if last_long is not None:
                miles += calculate_distance(
                    last_lat,
                    last_long,
                    lat,
                    lon)
            last_long=lon
            last_lat=lat
    print(start_time, end_time)
    print("Total miles: " + str(miles))

    date = input("Date: ")
    p = input("Purpose: ")


    date_url = date.replace("/", "-")



    m = folium.Map(location=path[0], zoom_start=6)
    folium.PolyLine(
        path, color="blue", weight=5, opacity=0.8
    ).add_to(m)

    for mk in new_file_markers:
        mk.add_to(m)

    m.save(os.path.join(details, date_url + ".html"))


    f = open(os.path.join(details, date_url + ".json"), "w")
    f.write(json.dumps(gps_data))
    f.close()

    zip = zipfile.ZipFile(os.path.join(details, date_url + ".zip"), "w", zipfile.ZIP_DEFLATED)
    for j in sorted(os.listdir(jsonOut)):
        zip.write(os.path.join(jsonOut, j), arcname=j)
    zip.close()


    f = open(os.path.join(records, "master.csv"), "a")
    w = csv.writer(f)


    w.writerow([
        date,
        start_time,
        end_time,
        get_address(*start_location) + f" AKA {start_location}",
        get_address(*end_location) + f" AKA {start_location}",
        miles,
        p,
        "details/" + date_url + ".json",
        "details/" + date_url + ".html"


    ])

    f.close()

if __name__ == "__main__":
    main()