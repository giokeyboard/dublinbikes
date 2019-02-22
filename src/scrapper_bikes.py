# Program to scrap dynamic and static data from JCDecaux
# Sending all to MySQL DB

import requests  # to send the request to the API
# is BeautifulSoup package necessary for this module?
# from bs4 import BeautifulSoup
import time  # to set the delay time of invoking the API
import pymysql  # to set up the database connection

HOST = "dublinbikes.cb2pu3bkmmlf.us-east-2.rds.amazonaws.com"
USERNAME = "master"
PASSWORD = "master-50"
DATABASE = "dublinbikes"


def get_count():
    """function to call the JCDecaux API and parse the JSON data"""

    url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e91c3125a3ebb07cf4eb407dee6251d324dfba9c"

    # Request with fake header
    # To avoid 403 HTTP error that might arise
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Parse the JSON
    data = r.json()

    return data


def station():
    """function to parse and store static data from JSON in database"""

    # store JSON data in a variable
    value = get_count()
    # create db connection object
    db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

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
        # SQL query to insert data in stations table
        sql = """INSERT INTO dublinbikes.station (address,banking,bike_stands,bonus,contract_name,number,
        position_lat,position_lng,status) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (address_d,
                                                                                                      banking_d,
                                                                                                      bike_stands_d,
                                                                                                      bonus_d,
                                                                                                      contact_name_d,
                                                                                                      number_d,
                                                                                                      position_lat_d,
                                                                                                      position_lng_d,
                                                                                                      status_d)
        try:
            print("Line 1 ")
            cursor.execute(sql)  # Execute the SQL command
            print(cursor._last_executed)
            # print("Line 2")
            db.commit()  # Commit your changes in the database
            print("data inserted successfully")

        except:
            # rollback in case there is any error
            db.rollback()
            # print(cursor._last_executed)
            print("Not working")

    # disconnect from server
    db.close()


# call station function to get and store the static data in the database
station()

while True:
    # print(get_count())   #Calling the function after a delay of 300 seconds or 5 minutes
    value = get_count()  # Calling the get_count function to invoke the API
    # Open database connection
    db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    for i in range(0, len(value)):
        value_1 = value[i]
        number_d = value_1['number']
        # print("Number is",station_id)
        available_bikes_d = value_1['available_bikes']
        # print("Station is",station_name)
        available_bike_stands_d = value_1['available_bike_stands']
        # print("Available is",number_bikes_available)
        # print(type(number_bikes_available))
        # Save event data to database
        last_update_d = value_1['last_update']
        # Prepare QL query to INSERT a record into the database.
        # sql= """INSERT INTO mydb.dynamic_data_6 (available) VALUES ('%s')""" % (number_bikes_available)
        sql = """INSERT INTO dublinbikes.availability (number,available_bikes,available_bike_stands,last_update) 
        VALUES ('%s','%s','%s','%s')""" % (number_d, available_bikes_d, available_bike_stands_d, last_update_d)
        try:
            print("Line 1 ")
            cursor.execute(sql)  # Execute the SQL command
            print(cursor._last_executed)
            # print("Line 2")
            db.commit()  # Commit your changes in the database
            print("data inserted successfully")

        except:
            # rollback in case there is any error
            db.rollback()
            # print(cursor._last_executed)
            print("Not working")

    # disconnect from server
    db.close()

    time.sleep(400)
    # VALUES ('%s','%s','%s','%s','%s','%s')""" % (1,Tweet.text,User.screen_name,score,search_type,User.location)
