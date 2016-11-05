from flask import Flask, render_template , jsonify ,request
from flask_bootstrap import Bootstrap
from collections import Counter
import pycountry
import csv


app = Flask(__name__,static_url_path='/static')
Bootstrap(app)


@app.route("/")
def index():
    return render_template('base.html')


@app.route("/smallMultiple")
def smallMultiple():
    return render_template('smallMultiple.html')


@app.route("/barChart")
def barChart():
    return render_template('barChart.html')


@app.route("/survivorsVsFlightType")
def survivorsVsFlightType():
    cnt = Counter()
    with open('static/data/data.csv', 'rb') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',')
        for row in dataReader:
            if row[9] == "Aboard":
                continue
            if row[9] != "?" and row[10] != "?":
                cnt[row[6].split(" ")[0]] += int(row[9])-int(row[10])
        print cnt.most_common(10)
        result = [{'TypeOfFlight':key, 'noOfSurvivors':value} for key,value in cnt.items()]
        return jsonify(result)


@app.route("/yearVsAccidents")
def yearVsAccidents():
    result = []

    with open('static/data/data.csv', 'rb') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',')
        for row in dataReader:
            if row[9] == "Aboard":
                continue
            if len(row) == 15 and row[13] != "?":
                year = row[0].split(",")[1]
                location = row[2]
                operator = row[3]
                aircraftType = row[6]
                aboard = row[9]
                fatalities = row[10]
                latitude = row[13]
                longitude = row[14]
                summary = row[12]

                if(fatalities == "?"):
                    fatalities = 0
                if(int(fatalities) == 0 ):
                    fatalitiesNameBasedOnCount = 'nofatalities'
                else:
                    fatalitiesNameBasedOnCount = 'fatalities'
                 
                content = {
                    "name": operator,
                    "year": year,
                    "location": location,
                    "operator": operator,
                    "aircraftType": aircraftType,
                    "aboard": aboard,
                    "fatalities": fatalities,
                    "latitude": latitude,
                    "longitude": longitude,
                    "fillKey" : fatalitiesNameBasedOnCount,
                    "summary": summary
                }
                result.append(content)
        return jsonify(result)

        #     if row[9] == "Aboard":
        #         continue
        #     if row[9] != "?" and row[10] != "?":
        #         cnt[row[6].split(" ")[0]] += int(row[9])-int(row[10])
        # print cnt.most_common(10)
        # result = [{'TypeOfFlight':key, 'noOfSurvivors':value} for key,value in cnt.items()]
        # return jsonify(result)

# @app.route("/sales.csv")
# def hello1():
#     return app.send_static_file('sales.csv')


@app.route("/yearVsAccidentsArea")
def yearVsAccidentsArea():

    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha2
    result = []

    with open('static/data/data.csv', 'rb') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',')
        for row in dataReader:
            if row[9] == "Aboard":
                continue
            if row[2] != "?":
                if "," in row[2]:
                    print "Part of the Name: " , row[2].split(",")[1].strip() , countries.get(row[2].split(",")[1].strip(), 'Unknown code')
                    if (countries.get(row[2].split(",")[1].strip(), 'Unknown code') == 'Unknown code'):
                        result.append(row[2].split(",")[1].strip())
                else:
                    print "Entire Name: " , row[2].strip() , countries.get(row[2].strip(), 'Unknown code') 
                    if ( countries.get(row[2].strip(), 'Unknown code') == 'Unknown code'):
                        result.append(row[2].strip())

        # print countries
        print len(set(result))
        #     if len(row) == 15:
        #         year = row[0].split(",")[1]
        #         location = row[2]
        #         operator = row[3]
        #         aircraftType = row[6]
        #         aboard = row[9]
        #         fatalities = row[10]
        #         latitude = row[13]
        #         longitude = row[14]
        #         summary = row[12]

        #         if(fatalities == "?"):
        #             fatalities = 0
        #         if(int(fatalities) == 0 ):
        #             fatalitiesNameBasedOnCount = 'nofatalities'
        #         else:
        #             fatalitiesNameBasedOnCount = 'fatalities'
                 
        #         content = {
        #             "name": operator,
        #             "year": year,
        #             "location": location,
        #             "operator": operator,
        #             "aircraftType": aircraftType,
        #             "aboard": aboard,
        #             "fatalities": fatalities,
        #             "latitude": latitude,
        #             "longitude": longitude,
        #             "fillKey" : fatalitiesNameBasedOnCount,
        #             "summary": summary
        #         }
        #         result.append(content)
        # return jsonify(result)

if __name__ == "__main__":
    app.run(port=8001,debug=True)

