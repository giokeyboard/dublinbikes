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
    data=list(data)
   

    

    return render_template('Dublin_bike_2.html',data=data)

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

if __name__=='__main__':
    app.run(debug=True)
