from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    memo = db.Column(db.String(100))

st=dt.datetime.now()
st_h=st.hour
st_m=st.minute

@app.route("/", methods=['GET', 'POST'])
def index():
    et=dt.datetime.now()
    et_h=et.hour
    et_m=et.minute
    day=dt.datetime.now().date()
    
    if et_m < st_m:
        th=et_h-st_h-1
        tm=et_m-st_m+60
    else:
        th=et_h-st_h
        tm=et_m-st_m
        
    if request.method == 'POST':
        
        username = request.form.get('username')
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return render_template('home.html', day=day, st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m, th=th, tm=tm)
    
    else:
        return render_template('index.html', day=day, st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m, th=th, tm=tm)

@app.route('/home', methods=['GET', 'POST'])
def home():
    
    et=dt.datetime.now()
    et_h=et.hour
    et_m=et.minute
    
    if et_m < st_m:
        th=et_h-st_h-1
        tm=et_m-st_m+60
    else:
        th=et_h-st_h
        tm=et_m-st_m
    
    username = request.form.get('username')
    
    if request.method == 'POST':    
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return render_template('home.html', user=user, username=username, st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m, th=th, tm=tm)
    
    else:
        return render_template('home.html', st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m, th=th, tm=tm)    
    
@app.route('/finish', methods=['GET', 'POST'])
def finish():
    et=dt.datetime.now()
    et_h=et.hour
    et_m=et.minute
    
    if et_m < st_m:
        th=et_h-st_h-1
        tm=et_m-st_m+60
    else:
        th=et_h-st_h
        tm=et_m-st_m

    return render_template('finish.html', st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m, th=th, tm=tm)
           
@app.route('/history', methods=['GET', 'POST'])
def history():
    user = User.query.all()
    return render_template('history.html', user=user)

if __name__=='__main__':
    app.run(debug=True)