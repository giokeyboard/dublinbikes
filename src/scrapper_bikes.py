# Program to scrap data from JCDecaux API and store the response JSON data into the database

import requests  # to send the request to the API
# from bs4 import BeautifulSoup
import time  # to set the delay time of invoking the API
import pymysql  # to set up the database connecction
from datetime import date  # to get the date and time of the system
import datetime  # to get hours, minutes and date
import calendar  # to get the day of the week

HOST = "dublinbikes.cb2pu3bkmmlf.us-east-2.rds.amazonaws.com"
USERNAME = "master"
PASSWORD = "master-50"
DATABASE = "dublinbikes"


def get_count():  # Function to call the API
    """
    function to call the JCDecaux API and parse the JSON data
    :return: JSON file
    """
    url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e91c3125a3ebb07cf4eb407dee6251d324dfba9c"

    # Request with fake header, otherwise you will get an 403 HTTP error sometimes. It might work without this as well
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Parse the JSON
    data = r.json()

    return data


def station():  # function to store the static data into the database
    """
    function to parse and store static data from JSON in database
    :return: none
    """
    value = get_count()
    db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
    cursor = db.cursor()  # prepare a cursor object using cursor() method
    for i in range(0, len(value)):
        value_1 = value[i]
        address_d = value_1['address']
        banking_d = value_1['banking']
        bike_stands_d = value_1['bike_stands']
        bonus_d = value_1['bonus']
        contact_name_d = value_1['contract_name']
        number_d = value_1['number']
        position_lat_d = value_1['position']['lat']
        position_lng_d = value_1['position']['lng']
        status_d = value_1['status']
        sql = """INSERT INTO dublinbikes.station (address,banking,bike_stands,bonus,contract_name,number,
        position_lat,position_lng,status) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (
            address_d, banking_d, bike_stands_d, bonus_d, contact_name_d, number_d, position_lat_d, position_lng_d,
            status_d)
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


station()


def get_day():  # function to get the day of the week corresponding to the day when data is fetched
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
    day = get_day()  # Calling the get_day function and store the returned data
    time_hr = get_hour()
    mins = get_mins()
    date_d = get_date()
    date_s = str(date_d)  # Convert date to string
    print(day)  # Control print statement
    print(date_s)  # Control print statement

    value = get_count()  # Calling the get_count function to invoke the API
    db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)  # Open database connection
    cursor = db.cursor()  # prepare a cursor object using cursor() method
    for i in range(0, len(value)):
        value_1 = value[i]
        number_d = value_1['number']
        available_bikes_d = value_1['available_bikes']
        available_bike_stands_d = value_1['available_bike_stands']
        last_update_d = value_1['last_update']
        # Prepare SQL query to INSERT a record into the database.
        # sql= """INSERT INTO mydb.dynamic_data_6 (available) VALUES ('%s')""" % (number_bikes_available)
        sql = """INSERT INTO dublinbikes.availability (number,available_bikes,available_bike_stands,last_update,
        day_of_week,hour_d,mins,date_of_fetching) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')""" % (
            number_d, available_bikes_d, available_bike_stands_d, last_update_d, day, time_hr, mins, date_s)
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

    time.sleep(400)  # A delay of 400 seconds after which invoke or send request to JCDecaux API
