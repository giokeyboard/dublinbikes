from flask import Flask, render_template,json,request
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
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
        sys.exit('error',e)

    cur = con.cursor()
    cur.execute("SELECT * FROM dublinbikes.station")
    data = cur.fetchall()
    
    cur4= con.cursor()
    cur4.execute("SELECT temperature,wind_speed,cloud_coverage FROM (SELECT * FROM weather ORDER BY id DESC LIMIT 1)sub ")
    data4=cur4.fetchone()
    
    data=list(data)
    data4=list(data4)
    print(data)
    print(data4)

    

    return render_template('Copy_Dublin_bike_2_v2_cleaned.html',data=data,data4=data4)

@app.route("/update", methods=['GET','POST'])
def update():
    post = request.args.get('post', 0, type=int)
    print(post)
    post=int(post)
    print(type(post))
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
        sys.exit('error',e)
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
    post2 = request.args.get('post', 0, type=int)
    print(post2)
    post=int(post2)
    print(type(post2))
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
        sys.exit('error',e)
    cur2= con.cursor()
    cur2.execute("SELECT number,available_bikes,available_bike_stands FROM availability where ID in (SELECT max(ID) FROM (select * from (select * from availability order by id Desc limit 226) sub order by id asc)as T GROUP BY number )  order by ID")
    data2=cur2.fetchall()
    print(type(data2))
    
    print(data2)
    print(len(data2))
    
    return json.dumps(data2);

@app.route("/weather", methods=['GET','POST'])
def weather():
    post = request.args.get('post', 0, type=int)
    print(post)
    post=int(post)
    print(type(post))
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
        sys.exit('error',e)
    cur5= con.cursor()
    cur5.execute("SELECT temperature,wind_speed,cloud_coverage FROM (SELECT * FROM weather ORDER BY id DESC LIMIT 1)sub ")
    data5=cur5.fetchone()
    
    
    print(type(data5))
    
    print(data5)
    print(len(data5))
    
    return json.dumps(data5);





if __name__=='__main__':
    app.run(debug=True)
