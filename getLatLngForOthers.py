import csv
import requests
count = 0
with open("data/updatedData.csv", 'w') as writeFile:
    thedatawriter = csv.writer(writeFile)
    thedatawriter.writerow(["Date", "Time", "Location","Operator", "Flight No", "Route","AC Type", "Registration", "CN / LM","Aboard", "Fatalities", "Ground", "Summary", "Latitude", "Longitude"])
    with open( "data/allUpdatedData.csv", 'rb') as mycsvfile:
        csvReader = csv.reader(mycsvfile)
        for row in csvReader:
            if count == 0:
                pass
                count += 1
            else:
                count += 1
                if len(row) == 13:
                    location = row[2]
                    if "," in location:
                        location = location.split(",")[1]
                    elif " " in location:
                        location = location.split(" ")[1]
                    else:
                        location
                    if location.strip() == "":
                        location = row[2]
                    # print location
                    url = "https://maps.googleapis.com/maps/api/geocode/json?address="+location+"&key=AIzaSyDhSP5Zdh585tFm5UyHx8QvRe2Wb6jJsHk"
                    r = requests.get(url)
                    if r.json()['status'] != "ZERO_RESULTS":
                        lat = r.json()['results'][0]['geometry']['location']['lat']
                        lng = r.json()['results'][0]['geometry']['location']['lng']
                        row.append(lat)
                        row.append(lng)
                    else:
                        print "No results for: " , count , location
                thedatawriter.writerow(row)
                

