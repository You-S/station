from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
import calendar
import os

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Authorization

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stationData.db'
db = SQLAlchemy(app)
app.secret_key = 'secret'
app.permanent_session_lifetime = timedelta(minutes=60)

class Station(db.Model):
    __tablename__ = 'stationData'
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    name = db.Column(db.String(50))
    yomi = db.Column(db.String(50))
    address = db.Column(db.String(50))
    lon = db.Column(db.String(20))
    lat = db.Column(db.String(20))
    linename = db.Column(db.String(50))
    linenameC = db.Column(db.String(50))
    pref = db.Column(db.String(50))
    
@app.route('/')
def index():
    i = random.randint(1,10865)
    station = Station.query.filter_by(id=i)
    return render_template('index.html', station=station)

@app.route('/check', methods=['POST'])
def check():
    answer = request.form['answer']
    colect = request.form['colect']
    if answer == colect:
        result = "正解"
        if 'counter' in session:
            session['counter'] += 1
        else:
            session['counter'] = 1
    else:
        result = "不正解"
        session['counter'] = 0
    # print(answer,comment,colect)
    counter = session['counter']
    return render_template('result.html', result=result, answer=answer, colect=colect,counter=counter)  

if __name__ == '__main__':
    port = os.getenv("PORT")
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)