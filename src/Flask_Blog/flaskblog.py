from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
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
    cur2= con.cursor()
    cur2.execute("SELECT * FROM availability where ID in (SELECT max(ID) FROM (select * from (select * from availability order by id Desc limit 226) sub order by id asc)as T GROUP BY number )  order by ID")
    data2=cur2.fetchall()
    
    data=list(data)
    data2=list(data2)
    print(data)
    print(data2)

    

    return render_template('Copy_Dublin_bike_2_v2_cleaned.html',data=data,data2=data2)

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

if __name__=='__main__':
    app.run(debug=True)
