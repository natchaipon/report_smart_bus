# import mysql.connector
from flask import Flask, render_template, request
import requests
import json
import datetime

app = Flask(__name__)


@app.route('/index_chart_month')
def index_chart_month():
    x = datetime.datetime.now()
    # print(x.year)
    data = requests.get('http://localhost:5000/select_sum_month/1/' + str(x.year))
    result = data.json()
    bus_box_table = []
    bus_rfid_table = []

    for i in result:
        if i["bus_id"] == "bus_box_table":
            bus_box_table.append(i)

        if i["bus_id"] == "bus_rfid_table":
            bus_rfid_table.append(i)

    return render_template('line_chart_month.html', json_bus_box_table = bus_box_table , json_bus_rfid_table = bus_rfid_table , bus_id = 1)
    # return render_template('test_.html', json_bus_box_table = bus_box_table , json_bus_rfid_table = bus_rfid_table)


@app.route('/chart_month', methods = ['POST', 'GET'])
def chart_month():
    year_input = request.form['year_input']
    # print(year_input)
    bus_id = request.form['bus_id']
    bus_id = bus_id.split(" ")
    url = 'http://localhost:5000/select_sum_month/{0}/{1}'.format(bus_id[1], year_input)
    data = requests.get(url)
    result = data.json()

    bus_box_table = []
    bus_rfid_table = []

    for i in result:
        if i["bus_id"] == "bus_box_table":
            bus_box_table.append(i)

        if i["bus_id"] == "bus_rfid_table":
            bus_rfid_table.append(i)

    return render_template('line_chart_month.html', json_bus_box_table = bus_box_table , json_bus_rfid_table = bus_rfid_table , bus_id = bus_id[1])


@app.route('/index_chart_year')
def index_chart_year():
    x = datetime.datetime.now()
    # print(x.year)
    data = requests.get('http://localhost:5000/select_sum_year/1')
    result = data.json()
    bus_box_table = []
    bus_rfid_table = []

    for i in result:
        if i["bus_id"] == "bus_box_table":
            bus_box_table.append(i)

        if i["bus_id"] == "bus_rfid_table":
            bus_rfid_table.append(i)

    return render_template('line_chart_year.html', json_bus_box_table = bus_box_table , json_bus_rfid_table = bus_rfid_table , bus_id = 1)
    

@app.route('/chart_year' , methods = ['POST', 'GET'])
def line_chart_year():
    bus_id = request.form['bus_id']
    bus_id = bus_id.split(" ")

    data = requests.get('http://localhost:5000/select_sum_year/' + str(bus_id[1]))
    result = data.json()
    bus_box_table = []
    bus_rfid_table = []

    for i in result:
        if i["bus_id"] == "bus_box_table":
            bus_box_table.append(i)

        if i["bus_id"] == "bus_rfid_table":
            bus_rfid_table.append(i)

    return render_template('line_chart_year.html', json_bus_box_table = bus_box_table , json_bus_rfid_table = bus_rfid_table , bus_id = bus_id[1])



@app.route('/index_cal_sum_date')
def index_cal_sum_date():
    return render_template('cal_sum_date.html')


@app.route('/cal_sum_date' , methods = ['POST', 'GET'])
def cal_sum_date():
    bus_id = request.form['bus_id']
    bus_id = bus_id.split(" ")
    previous = request.form['previous']
    previous = previous.split("/")
    next_ = request.form['next']
    next_ = next_.split("/")

    previous_ = str(previous[2]) + "-" + str(previous[0]) + "-" + str(previous[1])
    next_c = str(next_[2]) + "-" + str(next_[0]) + "-" + str(next_[1])

    cal = previous_ + "=>" + next_c
    print(cal)

    url = 'http://localhost:5000/select_sum_last_date/{0}/{1}'.format(bus_id[1] , cal)
    data = requests.get(url)
    result = data.json()

    return render_template('cal_sum_date.html' , previous = result[0]["resule"] , next = result[1]["resule"] , bus_id = bus_id[1] , date = cal)

@app.route('/')
def dashboard():
    return render_template('index_dashboard.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)