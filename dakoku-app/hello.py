from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime
from sqlalchemy import distinct

# database 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# todo list
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# user attendance
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    starth = db.Column(db.String(20), nullable=False)
    startm = db.Column(db.String(20), nullable=False)
    
# Absence message
mail = Mail(app)


st=datetime.now()
st_h=st.hour
st_m=st.minute

# Attendance

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html', st_h=st_h, st_m=st_m)

# home
# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     st=datetime.now()
#     st_h=st.hour
#     st_m=st.minute
    
#     if request.method == 'POST':   
#         day=datetime.now().date()
#         username = request.form.get('username')
        
#         newinfo = User(user=username, day=day, starth=st_h, startm=st_m)
#         db.session.add(newinfo)
#         db.session.commit()
#         users = User.query.all()
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         # namedate = User.query(User.starth, User.startm).all()
 
#         return render_template('home.html', users=users, tasks=tasks, username=username, st_h=st_h, st_m=st_m)
#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('home.html', tasks=tasks, st_h=st_h, st_m=st_m)      

# home
# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     st=datetime.now()
#     st_h=st.hour
#     st_m=st.minute
    
#     if request.method == 'POST':   
#         day=datetime.now().date()
#         username = request.form.get('username')
        
#         newinfo = User(user=username, day=day, starth=st_h, startm=st_m)
#         db.session.add(newinfo)
#         db.session.commit()
#         users = User.query.all()
#         tasks = Todo.query.order_by(Todo.date_created).all()
        
#         new = User.query.filter_by(user="中川崇大", day='2022-04-29')
        # for neo in new:
        #     if neo.starth == '19':
        #         aaa = neo.id
        #         ccc = User.query.get(aaa)
        #         db.session.delete(ccc)
        #         db.session.commit()
                

 
    #     return render_template('home.html', bbb=new, users=users, tasks=tasks, username=username, st_h=st_h, st_m=st_m)
    # else:
    #     tasks = Todo.query.order_by(Todo.date_created).all()
    #     return render_template('home.html', tasks=tasks, st_h=st_h, st_m=st_m)      

# home test
@app.route('/home', methods=['GET', 'POST'])
def home():
    st=datetime.now()
    st_h=st.hour
    st_m=st.minute
    
    if request.method == 'POST':
        
        day=datetime.now().date()
        username = request.form.get('username')
    
        check = User.query.filter_by(user=username, day=day).first()
    
        if check is None:
            newinfo = User(user=username, day=day, starth=st_h, startm=st_m)
            db.session.add(newinfo)
            db.session.commit()
           
        else:
            pass
 
        new = User.query.filter_by(user="tkhr", day='2022-04-29')
        for neo in new:
            if neo.starth == '20':
                aaa = neo.id
                # ccc = User.query.get(aaa)
                # db.session.delete(ccc)
                # db.session.commit()
                
        users = User.query.all()
        tasks = Todo.query.order_by(Todo.date_created).all()
            
 
        return render_template('home.html', bbb=new, check=check, users=users, tasks=tasks, username=username, st_h=st_h, st_m=st_m)
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', tasks=tasks, st_h=st_h, st_m=st_m)      


# Leaving
@app.route('/finish', methods=['GET', 'POST'])
def finish():
    if request.method == 'POST':
        
        username = request.form.get('username')
        day=datetime.now().date()
        
        # times = User.query
        time = User.query.filter_by(day=day).all()
        et=datetime.now()
        et_h=et.hour
        et_m=et.minute

        if et_m < st_m:
            th=et_h-st_h-1
            tm=et_m-st_m+60
        else:
            th=et_h-st_h
            tm=et_m-st_m
            
        return render_template('finish.html',time=time, et_h=et_h, et_m=et_m, th=th, tm=tm)
    else:
        return render_template('finish.html')


# Absence message
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

# calendar
@app.route('/history', methods=['GET', 'POST'])
def calendar():
    
    infos = User.query.all()
    # infos = session.query(distinct(User.day)).all()
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
    return render_template('history.html', events=events)


# todo 
@app.route('/memo', methods=['GET', 'POST'])
def aaa():
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('memo.html', tasks=tasks)


# add todo tasks
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


# remove todo tasks
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/memo')
    except:
        return 'エラー'


# debug
if __name__=='__main__':
    app.run(debug=True)