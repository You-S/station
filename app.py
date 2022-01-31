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
app.permanent_session_lifetime = timedelta(minutes=30)

class Station(db.Model):
    __tablename__ = 'station'
    id = db.Column(db.Integer, primary_key=True)
    stationNo = db.Column(db.Integer)
    stationUno = db.Column(db.Integer)
    name = db.Column(db.String(50))
    yomi = db.Column(db.String(50))
    lineid = db.Column(db.Integer)
    prefNo = db.Column(db.Integer)
    address = db.Column(db.String(50))
    lon = db.Column(db.String(20))
    lat = db.Column(db.String(20))

class Line(db.Model):
    __tablename__ = 'line'
    id = db.Column(db.Integer, primary_key=True)
    lineid = db.Column(db.Integer)
    linename = db.Column(db.String(50))
    lineCname = db.Column(db.String(50))
    
class Pref(db.Model):
    __tablename__ = 'pref'
    id = db.Column(db.Integer, primary_key=True)
    prefname = db.Column(db.String(50))
     
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        session['code'] = ''
        session['choiceno'] = ''
        return render_template('index.html')
    else:
        choice = request.form['choice']
        if choice == 'all':            
            fstation = Station.query.all()
            station = random.choice(fstation)
            return render_template('quiz.html', station=station)
        elif choice == 'line':
            line = Line.query.all()
            return render_template('line.html', line=line)
        else:
            pref = Pref.query.all()
            return render_template('pref.html', pref=pref)

@app.route('/quiz', methods=['POST'])
def quiz():
    if request.form['code'] == 'line':
        session['code'] = 'line'
        if session['choiceno'] == '':
            session['choiceno'] = request.form['secondchoice']
            choiceno = request.form['secondchoice']
        else:
            choiceno = session.get('choiceno')
        linecode = Line.query.filter_by(id=int(choiceno)).first()
        fstation = Station.query.filter_by(lineid=linecode.lineid).all()
        station = random.choice(fstation)
        return render_template('quiz.html', station=station)
    elif request.form['code'] == 'pref':
        session['code'] = 'pref'
        if session['choiceno'] == '':
            session['choiceno'] = request.form['secondchoice']
            choiceno = request.form['secondchoice']
        else:
            choiceno = session.get('choiceno')
        prefcode = Pref.query.filter_by(id=int(choiceno)).first()
        fstation = Station.query.filter_by(prefNo=prefcode.id).all()
        station = random.choice(fstation)
        return render_template('quiz.html', station=station)
    else:
        fstation = Station.query.all()
        station = random.choice(fstation)
        return render_template('quiz.html', station=station)
            
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
    counter = session['counter']
    code = session.get('code')
    return render_template('result.html', result=result, answer=answer, colect=colect, counter=counter, code=code)  

if __name__ == '__main__':
    port = os.getenv("PORT")
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)