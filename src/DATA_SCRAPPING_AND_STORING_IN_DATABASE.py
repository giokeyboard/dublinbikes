
# coding: utf-8

# In[ ]:


import requests    #to send the request to the API
from bs4 import BeautifulSoup
import time        #to set the delay time of invoking the API

import MySQLdb     #to set up the database connecction
HOST = "127.0.0.1"
USERNAME = "root"
PASSWORD = "Ganesha-46"
DATABASE = "mydb"


def get_count():   #function to call the api
    url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e91c3125a3ebb07cf4eb407dee6251d324dfba9c"
  

    # Request with fake header, otherwise you will get an 403 HTTP error sometimes. It might work without this as well
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Parse the JSON
    data = r.json()
   
    return data
while True:
    
    
   # print(get_count())   #Calling the function after a delay of 300 seconds or 5 minutes
    value=get_count()
    # Open database connection
    db = MySQLdb.connect(HOST,USERNAME, PASSWORD, DATABASE)
# prepare a cursor object using cursor() method
    cursor = db.cursor()
    for i in range(0,len(value)):
        value_1=value[i]
        station_id=value_1['number']
        print("Number is",station_id)
        station_name=value_1['name']
        print("Station is",station_name)
        number_bikes_available=value_1['available_bikes']
        print("Available is",number_bikes_available)
        #print(type(number_bikes_available))
        #Save event data to database

        # Prepare QL query to INSERT a record into the database.
        #sql= """INSERT INTO mydb.dynamic_data_6 (available) VALUES ('%s')""" % (number_bikes_available)
        sql = """INSERT INTO mydb.dynamic_data_7 (id,name,available) VALUES ('%s','%s','%s')""" % (station_id,station_name,number_bikes_available)
        try:
            print("Line 1 ")
            cursor.execute(sql) # Execute the SQL command
            print(cursor._last_executed)
            #print("Line 2")
            db.commit() # Commit your changes in the database
            print("data inserted successfully")
    
    
        except:
        
            db.rollback()
            print(cursor._last_executed)
            print("Not working")
        
        # Rollback in case there is any error
        
 # disconnect from server
    db.close()
    
    time.sleep(300)
    #VALUES ('%s','%s','%s','%s','%s','%s')""" % (1,Tweet.text,User.screen_name,score,search_type,User.location)


# In[ ]:




