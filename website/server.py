from flask import Flask, render_template , jsonify ,request, Response
from flask_bootstrap import Bootstrap
from collections import Counter
import pycountry
import csv

# Get list of all the countries in the ISO-Alpha3 format
# pycountry.countries.__dict__['objects'][0].__dict__['_fields']['alpha_3']
#for x in pycountry.countries.__dict__['objects']:
#   print x.__dict__['_fields']['alpha_3']
countries_alpha2 = [u'AW', u'AF', u'AO', u'AI', u'AX', u'AL', u'AD', u'AE', u'AR', u'AM', u'AS', u'AQ', u'TF', u'AG', u'AU', u'AT', u'AZ', u'BI', u'BE', u'BJ', u'BQ', u'BF', u'BD', u'BG', u'BH', u'BS', u'BA', u'BL', u'BY', u'BZ', u'BM', u'BO', u'BR', u'BB', u'BN', u'BT', u'BV', u'BW', u'CF', u'CA', u'CC', u'CH', u'CL', u'CN', u'CI', u'CM', u'CD', u'CG', u'CK', u'CO', u'KM', u'CV', u'CR', u'CU', u'CW', u'CX', u'KY', u'CY', u'CZ', u'DE', u'DJ', u'DM', u'DK', u'DO', u'DZ', u'EC', u'EG', u'ER', u'EH', u'ES', u'EE', u'ET', u'FI', u'FJ', u'FK', u'FR', u'FO', u'FM', u'GA', u'GB', u'GE', u'GG', u'GH', u'GI', u'GN', u'GP', u'GM', u'GW', u'GQ', u'GR', u'GD', u'GL', u'GT', u'GF', u'GU', u'GY', u'HK', u'HM', u'HN', u'HR', u'HT', u'HU', u'ID', u'IM', u'IN', u'IO', u'IE', u'IR', u'IQ', u'IS', u'IL', u'IT', u'JM', u'JE', u'JO', u'JP', u'KZ', u'KE', u'KG', u'KH', u'KI', u'KN', u'KR', u'KW', u'LA', u'LB', u'LR', u'LY', u'LC', u'LI', u'LK', u'LS', u'LT', u'LU', u'LV', u'MO', u'MF', u'MA', u'MC', u'MD', u'MG', u'MV', u'MX', u'MH', u'MK', u'ML', u'MT', u'MM', u'ME', u'MN', u'MP', u'MZ', u'MR', u'MS', u'MQ', u'MU', u'MW', u'MY', u'YT', u'NA', u'NC', u'NE', u'NF', u'NG', u'NI', u'NU', u'NL', u'NO', u'NP', u'NR', u'NZ', u'OM', u'PK', u'PA', u'PN', u'PE', u'PH', u'PW', u'PG', u'PL', u'PR', u'KP', u'PT', u'PY', u'PS', u'PF', u'QA', u'RE', u'RO', u'RU', u'RW', u'SA', u'SD', u'SN', u'SG', u'GS', u'SH', u'SJ', u'SB', u'SL', u'SV', u'SM', u'SO', u'PM', u'RS', u'SS', u'ST', u'SR', u'SK', u'SI', u'SE', u'SZ', u'SX', u'SC', u'SY', u'TC', u'TD', u'TG', u'TH', u'TJ', u'TK', u'TM', u'TL', u'TO', u'TT', u'TN', u'TR', u'TV', u'TW', u'TZ', u'UG', u'UA', u'UM', u'UY', u'US', u'UZ', u'VA', u'VC', u'VE', u'VG', u'VI', u'VN', u'VU', u'WF', u'WS', u'YE', u'ZA', u'ZM', u'ZW']
countries = [u'ABW', u'AFG', u'AGO', u'AIA', u'ALA', u'ALB', u'AND', u'ARE', u'ARG', u'ARM', u'ASM', u'ATA', u'ATF', u'ATG', u'AUS', u'AUT', u'AZE', u'BDI', u'BEL', u'BEN', u'BES', u'BFA', u'BGD', u'BGR', u'BHR', u'BHS', u'BIH', u'BLM', u'BLR', u'BLZ', u'BMU', u'BOL', u'BRA', u'BRB', u'BRN', u'BTN', u'BVT', u'BWA', u'CAF', u'CAN', u'CCK', u'CHE', u'CHL', u'CHN', u'CIV', u'CMR', u'COD', u'COG', u'COK', u'COL', u'COM', u'CPV', u'CRI', u'CUB', u'CUW', u'CXR', u'CYM', u'CYP', u'CZE', u'DEU', u'DJI', u'DMA', u'DNK', u'DOM', u'DZA', u'ECU', u'EGY', u'ERI', u'ESH', u'ESP', u'EST', u'ETH', u'FIN', u'FJI', u'FLK', u'FRA', u'FRO', u'FSM', u'GAB', u'GBR', u'GEO', u'GGY', u'GHA', u'GIB', u'GIN', u'GLP', u'GMB', u'GNB', u'GNQ', u'GRC', u'GRD', u'GRL', u'GTM', u'GUF', u'GUM', u'GUY', u'HKG', u'HMD', u'HND', u'HRV', u'HTI', u'HUN', u'IDN', u'IMN', u'IND', u'IOT', u'IRL', u'IRN', u'IRQ', u'ISL', u'ISR', u'ITA', u'JAM', u'JEY', u'JOR', u'JPN', u'KAZ', u'KEN', u'KGZ', u'KHM', u'KIR', u'KNA', u'KOR', u'KWT', u'LAO', u'LBN', u'LBR', u'LBY', u'LCA', u'LIE', u'LKA', u'LSO', u'LTU', u'LUX', u'LVA', u'MAC', u'MAF', u'MAR', u'MCO', u'MDA', u'MDG', u'MDV', u'MEX', u'MHL', u'MKD', u'MLI', u'MLT', u'MMR', u'MNE', u'MNG', u'MNP', u'MOZ', u'MRT', u'MSR', u'MTQ', u'MUS', u'MWI', u'MYS', u'MYT', u'NAM', u'NCL', u'NER', u'NFK', u'NGA', u'NIC', u'NIU', u'NLD', u'NOR', u'NPL', u'NRU', u'NZL', u'OMN', u'PAK', u'PAN', u'PCN', u'PER', u'PHL', u'PLW', u'PNG', u'POL', u'PRI', u'PRK', u'PRT', u'PRY', u'PSE', u'PYF', u'QAT', u'REU', u'ROU', u'RUS', u'RWA', u'SAU', u'SDN', u'SEN', u'SGP', u'SGS', u'SHN', u'SJM', u'SLB', u'SLE', u'SLV', u'SMR', u'SOM', u'SPM', u'SRB', u'SSD', u'STP', u'SUR', u'SVK', u'SVN', u'SWE', u'SWZ', u'SXM', u'SYC', u'SYR', u'TCA', u'TCD', u'TGO', u'THA', u'TJK', u'TKL', u'TKM', u'TLS', u'TON', u'TTO', u'TUN', u'TUR', u'TUV', u'TWN', u'TZA', u'UGA', u'UKR', u'UMI', u'URY', u'USA', u'UZB', u'VAT', u'VCT', u'VEN', u'VGB', u'VIR', u'VNM', u'VUT', u'WLF', u'WSM', u'YEM', u'ZAF', u'ZMB', u'ZWE', u'SOL']

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


@app.route("/choropleth")
def choropleth():
    return render_template('choropleth.html')


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
        # print cnt.most_common(10)
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
            if len(row) == 16 and row[13] != "?":
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



@app.route("/yearVsAccidentsArea/<year>.csv")
def yearVsAccidentsArea(year):
    cnt = Counter()
    with open('static/data/data.csv', 'rb') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',')
        for row in dataReader:
            if row[9] == "Aboard":
                continue
            if row[0].split(",")[1].strip() == year and row[15] != "ERR:15:no country code found" and row[15] != "?" :
                cnt[row[15]] += 1
    countriesPresent = [];
    def generate():
        yield "country" + "," + "numberofaccidents" + "\n"
        for key,value in cnt.items():
            if key in countries_alpha2:
                countriesPresent.append(pycountry.countries.get(alpha_2=key).alpha_3)
                yield pycountry.countries.get(alpha_2=key).alpha_3 + "," + str(value) + "\n"
        for country in countries:
            if country not in countriesPresent:
                yield country + "," + str(0) + "\n"
    return Response(generate(), mimetype='text/csv')



if __name__ == "__main__":
    app.run(port=8001,debug=True)

