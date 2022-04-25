from ensurepip import bootstrap
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime
from flask_bootstrap import Bootstrap


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    starth = db.Column(db.String(20), nullable=False)
    startm = db.Column(db.String(20), nullable=False)
    

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
    day=datetime.now().date()
    username = request.form.get('username')
    et=datetime.now()
    et_h=et.hour
    et_m=et.minute
    
    if request.method == 'POST':   
 
        newinfo = User(user=username, day=day, starth=st_h, startm=st_m)
        db.session.add(newinfo)
        db.session.commit()
        
        users = User.query.all()
        
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', users=users, tasks=tasks, username=username, st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m)
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', tasks=tasks, st_h=st_h, st_m=st_m, et_h=et_h, et_m=et_m)    
    
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



infos = User.query.all()

events = []

for info in infos:
    
    if int(info.starth) >= 11 and int(info.startm) >= 0:
    
        list = {
                'title': '遅刻',
                'date': info.day
            }
    else:
        list = {
                'title': '出勤',
                'date': info.day
            }
    
        
    events.append(list)
    # events = set(events)
    
    


@app.route('/history')
def calendar():
    return render_template('history.html', events=events)

@app.route('/memo', methods=['GET', 'POST'])
def aaa():
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('memo.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def memo():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(memo=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/memo')
        except:
            return "エラー"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('memo.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/memo')
    except:
        return 'エラー'



if __name__=='__main__':
    app.run(debug=True)