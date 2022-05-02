from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime
import random

# データベース
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Todo
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# ユーザー情報
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    starth = db.Column(db.String(20), nullable=False)
    startm = db.Column(db.String(20), nullable=False)
    
# 欠勤メッセージ
mail = Mail(app)

# ランダム用
rand = random.random()

# 出勤
@app.route("/", methods=['GET', 'POST'])
def index():

    st=datetime.now() # メッセージ内容のバリエーションのため
    st_h=st.hour
    st_m=st.minute
    return render_template('index.html',rand=rand, st_h=st_h, st_m=st_m)

# ホーム ヘッダーから飛んだとき用
@app.route('/home/<user>', methods=['GET', 'POST'])
def userhome(user):
    st=datetime.now() # データベース用
    st_h=st.hour
    st_m=st.minute
    tasks = Todo.query.order_by(Todo.date_created).all() # Todoリスト取得
    return render_template('home.html',username=user, tasks=tasks, st_h=st_h, st_m=st_m)      

# ホーム 出勤ボタンを押したとき用
@app.route('/home', methods=['GET', 'POST'])
def home():
    st=datetime.now() # データベース用
    st_h=st.hour
    st_m=st.minute
    
    if request.method == 'POST':
        
        day=datetime.now().date()
        username = request.form.get('username')
        check = User.query.filter_by(user=username, day=day).first() # 重複チェック用
        if check is None:
            newinfo = User(user=username, day=day, starth=st_h, startm=st_m)
            db.session.add(newinfo)
            db.session.commit()
            msg = ""
        else:
            msg = "Welcome back!"
            pass
        tasks = Todo.query.order_by(Todo.date_created).all() # Todoリスト取得            
 
        return render_template('home.html',msg=msg ,tasks=tasks, username=username, st_h=st_h, st_m=st_m)


# 退勤
@app.route('/finish/<user>', methods=['GET', 'POST'])
def finish(user):
    if request.method == 'POST':
        
        # ユーザーと時刻をフィルター
        day=datetime.now().date()
        time = User.query.filter_by(user=user, day=day).first()
        
        et=datetime.now()  # 退勤時刻
        et_h=et.hour
        et_m=et.minute
        st_h=time.starth # データベースにある出勤時刻(時)
        st_m=time.startm # データベースにある出勤時刻(分)

        if et_m < int(st_m): # 労働時間の計算
            th=et_h-int(st_h)-1
            tm=et_m-int(st_m)+60
        else:
            th=et_h-int(st_h)
            tm=et_m-int(st_m)
            
        return render_template('finish.html',username=user, et_h=et_h, et_m=et_m, th=th, tm=tm)
    else:
        return render_template('finish.html')


# 欠勤メッセージ
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


# カレンダー
@app.route('/history/<user>', methods=['GET', 'POST'])
def calendar(user):
    
    # ユーザーのデータを取得
    infos = User.query.filter_by(user=user)

    events = []
    for info in infos:
        if int(info.starth) >= 11 and int(info.startm) >= 0: # 11時以降を遅刻判定
            list = {
                    'title': '遅刻',
                    'date': info.day
                }
        else:
            list = {
                    'title': '出勤',
                    'date': info.day
                }
        events.append(list) # 過去のデータ分の出勤記録も表示するためにappend
    return render_template('history.html',username=user, events=events)

# Todo
@app.route('/memo/<user>', methods=['GET', 'POST'])
def todo(user):
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('memo.html', tasks=tasks, username=user)


# タスク追加
@app.route('/add/<user>', methods=['GET', 'POST'])
def memo(user):
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(memo=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('memo.html',tasks=tasks, username=user)
        except:
            return "エラー"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('memo.html', tasks=tasks, username=user)


# タスク削除
@app.route('/delete/<user>/<int:id>')
def delete(user, id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('memo.html', tasks=tasks, username=user)
    except:
        return 'エラー'
    
@app.route('/game/<user>')
def game(user):
    return render_template('game.html', username=user)

@app.route('/game/counter')
def counter():
    return render_template('counter.html')

@app.route('/game/sudoku')
def sudoku():
    return render_template('sudoku.html')

# debug
if __name__=='__main__':
    app.run(debug=True)