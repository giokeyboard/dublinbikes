# Import packages
from flask import Flask, render_template,json,request
app = Flask(__name__)

# Load the trained ML model
import pickle
random_forest = pickle.load(open('final_prediction.pickle','rb'))
random_forest_stands = pickle.load(open("final_prediction_bike_stands.pickle","rb"))

@app.route("/")
@app.route("/home")
def home():
    """lauch the required HTML page"""

    return render_template('index.html',data=0)


@app.route("/testing", methods=['GET','POST'])
def testing():
    """Fetch static data from database"""

    import sys
    import pymysql
    import re

    host='dublinbikes.cb2pu3bkmmlf.us-east-2.rds.amazonaws.com'
    user = 'master'
    password = 'master-50'
    db = 'dublinbikes'

    try:
        con = pymysql.connect(host=host,user=user,password=password,db=db, use_unicode=True, charset='utf8')
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    except Exception as e:
        sys.exit(e)

    cur = con.cursor()
    cur.execute("SELECT * FROM dublinbikes.station")
    data3 = cur.fetchall()

    print(data3)
    return json.dumps(data3);


@app.route("/update", methods=['GET','POST'])
def update():
    """Fetch real-time data for click marker"""

    # Store the request from JS
    post = request.args.get('post', 0, type=int)

    print(post)
    post=int(post)
    print(type(post))

    # Only after import required packages
    import sys
    import pymysql
    import re

    host='dublinbikes.cb2pu3bkmmlf.us-east-2.rds.amazonaws.com'
    user = 'master'
    password = 'master-50'
    db = 'dublinbikes'

    try:
        con = pymysql.connect(host=host,user=user,password=password,db=db, use_unicode=True, charset='utf8')
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    except Exception as e:
        sys.exit(e)

    cur3 = con.cursor()
    sql_select_query = """SELECT * FROM (SELECT * FROM availability ORDER BY id DESC LIMIT 113)sub where number=%s"""
    cur3.execute(sql_select_query, (post, ))
    data3 = cur3.fetchone()

    print(type(data3))
    print(data3)
    print(len(data3))

    return json.dumps(data3);


@app.route("/all_available_details", methods=['GET','POST'])
def all_available_details():
    """Fetch both static and dynamic data from database"""

    # Store the request from JS
    post2 = request.args.get('post', 0, type=int)

    print(post2)
    post=int(post2)
    print(type(post2))

    # Only after import required packages
    import sys
    import pymysql
    import re

    host='dublinbikes.cb2pu3bkmmlf.us-east-2.rds.amazonaws.com'
    user = 'master'
    password = 'master-50'
    db = 'dublinbikes'

    try:
        con = pymysql.connect(host=host,user=user,password=password,db=db, use_unicode=True, charset='utf8')
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    except Exception as e:
        sys.exit(e)

    cur2= con.cursor()
    cur2.execute("SELECT station.number,available_bikes,available_bike_stands,address,position_lat,position_lng FROM station,(SELECT * FROM availability ORDER BY id DESC LIMIT 113)sub where station.number=sub.number")
    data2=cur2.fetchall()

    print(type(data2))
    print(data2)
    print(len(data2))

    return json.dumps(data2);


@app.route("/weather", methods=['GET','POST'])
def weather():
    """Fetch weathear real-time data"""

    # Store the request from JS
    post = request.args.get('post', 0, type=int)

    print(post)
    post=int(post)
    print(type(post))

    # Only after import required packages
    import sys
    import pymysql
    import re

    host='dublinbikes.cb2pu3bkmmlf.us-east-2.rds.amazonaws.com'
    user = 'master'
    password = 'master-50'
    db = 'dublinbikes'

    try:
        con = pymysql.connect(host=host,user=user,password=password,db=db, use_unicode=True, charset='utf8')
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    except Exception as e:
        sys.exit(e)

    cur5= con.cursor()
    cur5.execute("SELECT temperature,wind_speed,cloud_coverage FROM (SELECT * FROM weather ORDER BY id DESC LIMIT 1)sub ")
    data5=cur5.fetchone()

    print(type(data5))
    print(data5)
    print(len(data5))

    return json.dumps(data5);


@app.route("/plan_your_trip_weather_forecast", methods=['GET','POST'])
def plan_your_trip_weather_forecast():
    """Fetch weather forecast data from OpenWeather API based on time and date selected by the user"""

    # Store the request from JS
    post = request.args.get('post', 0, type=str)

    print(post)
    post=str(post)
    print(type(post))

    # Only after import required packages
    import requests

    def get_count():
        """Call the OpenWeather API"""

        url = "http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=a4822db1b5634c2e9e25209d1837cc69&units=metric"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        # Parse the JSON
        data = r.json()
        return data


    def invoke_from_javascript(post):
        """Fetch weather forecast based on time and date selected by the user"""

        value = get_count()
        inp1 = post
        for i in range(0,len(value['list'])):
            date=value['list'][i]['dt_txt']
            type(date)
            if(inp1==date):
                temp=value['list'][i]['main']['temp']
                cloud=value['list'][i]['weather'][0]['main']
                speed=value['list'][i]['wind']['speed']
                list_data=(temp,cloud,speed)
                print(temp)
                print(cloud)
                print(speed)

                return list_data

    data6=invoke_from_javascript(post)
    return json.dumps(data6);


@app.route("/prediction_model", methods=['GET','POST'])
def prediction_model():
    """Based on user's request for source/destination we invoke the required pickle file to predict available bikes/available bike stands"""

    import numpy as np

    # Store the request from JS
    post = request.args.get('post',0,type=str)
    post=post.split()

    print("Data to be sent to prediction model ",post)
    print(type(post))

    nearest_station_no=int(post[0])
    second_nearest_station_no=int(post[1])
    temp=int(post[2])
    wind_s= int(post[4])
    flag = int(post[5])
    day_week = post[6]
    hr_day = int(post[7])
    fri_flag=mon_flag=sat_flag=sun_flag=thur_flag=tue_flag=wed_flag=0
    clear_flag=clo_flag=drizzle_flag=fog_flag=mis_flag=rain_flag=0

    # Based on the selected day of the week the resulting flag is set as 1
    if(day_week=="Friday"):
        fri_flag = 1
    if(day_week=="Monday"):
        mon_flag = 1
    if(day_week=="Saturday"):
        sat_flag = 1
    if(day_week=="Sunday"):
        sun_flag = 1
    if(day_week=="Thursday"):
        thur_flag = 1
    if(day_week=="Tuesday"):
        tue_flag = 1
    if(day_week=="Wednesday"):
        wed_flag = 1

    # Based on the selected day of the week the resulting cloud coverage is set to 1
    cloud_cover=post[3]
    if(cloud_cover=="Clear"):
        clear_flag = 1
    if(cloud_cover=="Clouds"):
        clo_flag = 1
    if(cloud_cover=="Drizzle"):
        drizzle_flag = 1
    if(cloud_cover=="Fog"):
        fog_flag = 1
    if(cloud_cover=="Mist"):
        mis_flag = 1
    if(cloud_cover=="Rain"):
        rain_flag = 1

    if(flag==0): # Prediction for source
        predict_request = [[nearest_station_no,hr_day,0,temp,wind_s,fri_flag,mon_flag,sat_flag,sun_flag,thur_flag,tue_flag,wed_flag,clear_flag,clo_flag,drizzle_flag,fog_flag,mis_flag,rain_flag]]
        print(predict_request)

        predicted_available_bikes = random_forest.predict(predict_request)
        print("Predicted available bikes for nearest station is",int(predicted_available_bikes[0]))

        predict_request = [[second_nearest_station_no,hr_day,0,temp,wind_s,fri_flag,mon_flag,sat_flag,sun_flag,thur_flag,tue_flag,wed_flag,clear_flag,clo_flag,drizzle_flag,fog_flag,mis_flag,rain_flag]]
        print(predict_request)
        predicted_available_bikes_2 = random_forest.predict(predict_request)
        print("Predicted available bikes for second nearest station is",int(predicted_available_bikes_2[0]))

    if(flag==1): # Prediction for destination
        predict_request = [[nearest_station_no,hr_day,0,temp,wind_s,fri_flag,mon_flag,sat_flag,sun_flag,thur_flag,tue_flag,wed_flag,clear_flag,clo_flag,drizzle_flag,fog_flag,mis_flag,rain_flag]]
        print(predict_request)

        predicted_available_bikes = random_forest_stands.predict(predict_request)
        print("Predicted available bike stands for nearest station is",int(predicted_available_bikes[0]))

        predict_request = [[second_nearest_station_no,hr_day,0,temp,wind_s,fri_flag,mon_flag,sat_flag,sun_flag,thur_flag,tue_flag,wed_flag,clear_flag,clo_flag,drizzle_flag,fog_flag,mis_flag,rain_flag]]
        print(predict_request)
        predicted_available_bikes_2 = random_forest_stands.predict(predict_request)
        print("Predicted available bike stands for second nearest station is",int(predicted_available_bikes_2[0]))

    # Fetch the ML model output and return as JSON to client
    data_from_model=[int(predicted_available_bikes[0]),int(predicted_available_bikes_2[0])]
    return json.dumps(data_from_model);


if __name__=='__main__':
    app.run(debug=True)
