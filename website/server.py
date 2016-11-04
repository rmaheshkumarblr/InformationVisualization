from flask import Flask, render_template , jsonify ,request
from flask_bootstrap import Bootstrap
from collections import Counter
import csv


app = Flask(__name__,static_url_path='/static')
Bootstrap(app)

@app.route("/")
def index():
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


# @app.route("/sales.csv")
# def hello1():
#     return app.send_static_file('sales.csv')


if __name__ == "__main__":
    app.run(port=8001,debug=True)

