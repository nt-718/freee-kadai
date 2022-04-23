from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(255), nullable=False)
    due = db.Column(db.DateTime, nullable=False)

mail = Mail(app)

st=datetime.now()
st_h=st.hour
st_m=st.minute

@app.route("/", methods=['GET', 'POST'])
def index():

    day=datetime.now().date()

    if request.method == 'POST':
        global st, st_h, st_m
        st=datetime.now()
        st_h=st.hour
        st_m=st.minute
        return render_template('home.html', day=day, st_h=st_h, st_m=st_m)
    else:
        return render_template('index.html', day=day, st_h=st_h, st_m=st_m)

@app.route('/home', methods=['GET', 'POST'])
def home():
    username = request.form.get('username')
    et=datetime.now()
    et_h=et.hour
    et_m=et.minute
    
    if request.method == 'POST':    
        return render_template('home.html', username=username, st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m)
    else:
        return render_template('home.html', st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m)    
    
@app.route('/finish', methods=['GET', 'POST'])
def finish():
    if request.method == 'POST':
        
        et=datetime.now()
        et_h=et.hour
        et_m=et.minute

        if et_m < st_m:
            th=et_h-st_h-1
            tm=et_m-st_m+60
        else:
            th=et_h-st_h
            tm=et_m-st_m
            
        return render_template('finish.html', st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m, th=th, tm=tm)
    else:
        return render_template('finish.html', st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m, th=th, tm=tm)

@app.route("/message", methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        sd = request.form.get('sender')
        tt = request.form.get('title')
        tx = request.form.get('text')
        msg = Message("ここにタイトルがはいります",
                    sender=sd,
                    recipients=["nkgw817@icloud.com"])
        msg.body = tt
        msg.html = tx
        mail.send(msg)
        flash(f'A test message was sent to recipients.')
        return redirect(url_for('message'))
    return render_template('message.html')

events = [
    {
        'title': '欠勤',
        'date': '2022-04-23'
    },
    {
        'title': '遅刻',
        'date': '2022-04-10'
    }
]   

@app.route('/history')
def calendar():
    return render_template('history.html', events=events)

@app.route('/memo', methods=['GET', 'POST'])
def create():
    return render_template('memo.html')
    
@app.route('/end', methods=['GET', 'POST'])
def create2():
    if request.method == 'POST':
        note = request.form.get('note')
        due = request.form.get('due')
        due = datetime.strptime(str(due), '%Y-%m-%d')
        new_memo = Memo(memo=note, due=due)
        db.session.add(new_memo)
        db.session.commit()
        return render_template('memo.html')
    else:        
        memos = Memo.query.all()
        return render_template('memo.html', memos=memos)


if __name__=='__main__':
    app.run(debug=True)