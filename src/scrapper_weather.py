# Program to scrap data from OpenWeatherMap API and store the response JSON data into the database

import requests  # to send the request to the open weather API
# from bs4 import BeautifulSoup
import time  # to set the delay time of invoking the API
import pymysql  # to set up the database connecction
from datetime import date  # to get the system date and time
import datetime  # to get hours, minutes and date
import calendar  # to get the day of the week

HOST = "dublinbikes.cb2pu3bkmmlf.us-east-2.rds.amazonaws.com"
USERNAME = "master"
PASSWORD = "master-50"
DATABASE = "dublinbikes"


def get_count():  # function to call the API
    """
    function to call the OpenWeatherMap API and parse the JSON data
    :return: JSON file
    """
    url = "http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=a4822db1b5634c2e9e25209d1837cc69&units" \
          "=metric "
    # Request with fake header to avoid 403 HTTP error that might arise
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Parse the JSON
    data = r.json()

    return data


def get_day():  # function to get the day of the week
    """
    function to get the day of the week in plain text format
    :return: weekday in plain text format
    """
    my_date = date.today()
    return calendar.day_name[my_date.weekday()]


def get_hour():
    """
    function to get the time (hour) of fetching
    :return: hour as number
    """
    return datetime.datetime.now().hour


def get_mins():
    """
    function to get the time (minutes) of fetching
    :return: minutes as number
    """
    return datetime.datetime.now().minute


def get_date():
    """
    function to get the date of fetching
    :return: date of fetching, yyyy-mm-dd
    """
    return datetime.datetime.now().date()


while True:
    value = get_count()  # Store JSON data fetched from weather API in a variable
    temp = value['main']['temp']  # Extract the temperature
    speed = value['wind']['speed']  # Extract the wind speed
    cloud = value['weather'][0]['main']  # Extract the cloud coverage
    day = get_day()  # Extract the day of the week
    time_hr = get_hour()
    mins = get_mins()
    date = get_date()
    date = str(date)  # Convert date to string
    print(day)  # Control print statement
    print(date)  # Control print statement

    db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)  # create db connection object
    cursor = db.cursor()  # prepare a cursor object using cursor() method
    sql = """INSERT INTO dublinbikes.weather (temperature,day_of_week,wind_speed,cloud_coverage,hour_d,mins,
    date_of_fetching) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (
        temp, day, speed, cloud, time_hr, mins, date)
    try:
        print("Line 1 ")
        cursor.execute(sql)  # Execute the SQL command
        print(cursor._last_executed)
        # print("Line 2")
        db.commit()  # Commit your changes in the database
        print("data inserted successfully")
    except:
        # Rollback in case there is any error
        db.rollback()
        # print(cursor._last_executed)
        print("Not working")

    # disconnect from server
    db.close()

    time.sleep(900)  # A delay of 900 seconds or 15 minutes after which again a request is send to API
