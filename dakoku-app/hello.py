from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime
import pytz
import random
from sqlalchemy import true

# タイムゾーンの設定
jst = pytz.timezone('Asia/Tokyo')

# データベース
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Todo
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    memo = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # データベース中身チェック
    def __repr__(self):
        return f"Todo('{self.user}', '{self.memo}', '{self.date_created}')"
    
# ユーザー情報
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False) # 20文字以上入力してもなぜか追加されます。
    day = db.Column(db.String(20), nullable=False)
    starth = db.Column(db.String(20), nullable=False)
    startm = db.Column(db.String(20), nullable=False)
    absence = db.Column(db.Boolean, default=False, nullable=False)
    endh = db.Column(db.String(20), nullable=False, default=23)
    endm = db.Column(db.String(20), nullable=False, default=59)

    # データベース中身チェック    
    def __repr__(self):
        return f"User('{self.user}', '{self.day}', '{self.starth}:{self.startm}', '{self.endh}:{self.endm}', '{self.absence}')"
    
# Request
class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(200))
    date = db.Column(db.String(20), nullable=False)
    endh = db.Column(db.String(20), nullable=False)
    endm = db.Column(db.String(20), nullable=False)
    
    # データベース中身チェック  
    def __repr__(self):
        return f"Request('{self.user}', '{self.text}', '{self.date}', '{self.endh}:{self.endm}')"
    

    
# 欠勤メッセージ
mail = Mail(app)


# ランダム用
rand = random.random()


# 出勤
@app.route("/", methods=['GET', 'POST'])
def index():
    
    # メッセージ内容のバリエーションのために時間取得
    st=datetime.now(jst) 
    st_h=st.hour
    st_m=st.minute
    return render_template('index.html',rand=rand, st_h=st_h, st_m=st_m)


# ホーム ヘッダーから飛んだとき用
@app.route('/home/<user>', methods=['GET', 'POST'])
def userhome(user):
    
     # データベース用
    st=datetime.now(jst)
    st_h=st.hour
    st_m=st.minute   
    
    if request.method == 'POST':    
        
        # 管理者
        if user == 'Admin':                   
            usr = request.form.get('filtername')
            tasks = Todo.query.filter_by(user=user).order_by(Todo.date_created).all() # Todoリスト取得
            
            # Admin画面フィルター
            if usr == '': 
                users = User.query.order_by(User.day).all() # 全ユーザーリスト取得
            elif usr == 'all':
                users = User.query.order_by(User.day).all() # 全ユーザーリスト取得
            else:
                users = User.query.filter_by(user=usr).all() # 個別ユーザーリスト取得         
            return render_template('home.html',username=user, tasks=tasks,users=users, st_h=st_h, st_m=st_m)      
        
        # 管理者以外
        else:          
            tasks = Todo.query.filter_by(user=user).order_by(Todo.date_created).all() # Todoリスト取得
            users = User.query.order_by(User.day).all() # ユーザーリスト取得      
            return render_template('home.html',username=user, tasks=tasks,users=users, st_h=st_h, st_m=st_m)      
   
    else:
        tasks = Todo.query.filter_by(user=user).order_by(Todo.date_created).all() # Todoリスト取得
        users = User.query.order_by(User.day).all() # ユーザーリスト取得
        return render_template('home.html',username=user, tasks=tasks,users=users, st_h=st_h, st_m=st_m)      


# ホーム 出勤ボタンを押したとき用
@app.route('/home', methods=['GET', 'POST'])
def home():
    
    # データベース用
    st=datetime.now(jst)
    st_h=st.hour
    st_m=st.minute
    
    if request.method == 'POST':
        day=datetime.now(jst).date()
        username = request.form.get('username')
        
        # 名前を入力せずに出勤したときの処理
        if username == "":
            return redirect('/')
        
        # 管理者として出勤したときの処理
        elif username == "Admin":
            tasks = Todo.query.filter_by(user=username).order_by(Todo.date_created).all() # Todoリスト取得            
            users = User.query.order_by(User.day).all() # ユーザーリスト取得
            return render_template('home.html',tasks=tasks,users=users, username=username, st_h=st_h, st_m=st_m)
        
        # visualize.html用の処理
        elif username == "freee":  
            return render_template('visualize.html')        
        
        else:
            check = User.query.filter_by(user=username, day=day).first() # 重複チェック用
            
            # 初出勤
            if check is None:
                
                # 時刻を01:05のように表示
                if int(st_h) < 10:
                    sth = "0" + st_h
                else:
                    sth = st_h
                    
                if int(st_m) < 10:
                    stm = "0" + st_m
                else:
                    stm = st_m
                    
                newinfo = User(user=username, day=day, starth=sth, startm=stm)
                # データベースに追加
                db.session.add(newinfo)
                db.session.commit()
                msg = ""
            
            # 2度目以降の出勤
            else:
                msg = "Welcome back!"
                pass
            
            tasks = Todo.query.filter_by(user=username).order_by(Todo.date_created).all() # Todoリスト取得            
            users = User.query.order_by(User.day).all() # ユーザーリスト取得
            return render_template('home.html',msg=msg ,tasks=tasks,users=users, username=username, st_h=st_h, st_m=st_m)


# 退勤
@app.route('/finish/<user>', methods=['GET', 'POST'])
def finish(user):
    
    if request.method == 'POST':    
        # ユーザーと時刻をフィルター
        if user == "Admin":
            return redirect('/')
        
        day=datetime.now(jst).date()
        time = User.query.filter_by(user=user, day=day).first()
        
        et=datetime.now(jst)  # 退勤時刻
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
            
        # データベースの退勤時間を更新
        endtime = User.query.filter_by(user=user, day=day).first() 
        endtime.endh = et_h
        endtime.endm = et_m
        db.session.commit() 
            
        return render_template('finish.html',username=user, et_h=et_h, et_m=et_m, th=th, tm=tm)
    
    else:
        return render_template('finish.html')


# 欠勤メッセージ
@app.route("/message", methods=['GET', 'POST'])
def msg():
    
    if request.method == 'POST':
        day=datetime.now(jst).date()
        username = request.form.get('username')
        
        # 重複チェック
        absence = User.query.filter_by(user=username, day=day).first()
        
        if absence is None:
            newinfo = User(user=username, day=day, starth=23, startm=59, absence=True) # Trueにして追加
            db.session.add(newinfo)
            db.session.commit()
            return render_template('message.html')
        
        else:            
            absence.absence = True # Trueに更新
            db.session.commit()
        
        return render_template('message.html')
    

    # if request.method == 'POST':
    #     sd = request.form.get('sender')
    #     tt = request.form.get('title')
    #     tx = request.form.get('text')
    #     msg = Message("ここにタイトルがはいります",
    #                 sender=sd,
    #                 recipients=["nkgw817@icloud.com"])
    #     msg.body = tt
    #     msg.html = tx
    #     mail.send(msg)
    #     flash(f'A test message was sent to recipients.')
    #     return redirect(url_for('message'))
    # return render_template('message.html')



# カレンダー
@app.route('/history/<user>', methods=['GET', 'POST'])
def calendar(user):
    
    # ユーザーのデータを取得
    infos = User.query.filter_by(user=user)

    events = []
    for info in infos:
        if info.absence == True:
            list = {
                    'title': '欠勤',
                    'date': info.day,
                    'color': 'crimson'
                }
            
        elif int(info.starth) >= 11 and int(info.startm) >= 0: # 11時以降を遅刻判定
          
            if int(info.endh) >= 23 and int(info.endm) == 59:
            
                list = { # 遅刻 当日
                        'title':str(info.starth) + ":" + str(info.startm) + " ~ ",
                        'date': info.day,
                        'color': 'green'
                    }
            else:
                list = { # 遅刻 過去
                        'title':str(info.starth) + ":" + str(info.startm) + " ~ " + str(info.endh) + ":" + str(info.endm),
                        'date': info.day,
                        'color': 'green'
                    }
        else:
            if int(info.endh) >= 23 and int(info.endm) == 59:
                list = { # 出勤 当日
                        'title':str(info.starth) + ":" + str(info.startm) + " ~ ",
                        'date': info.day,
                        'color': 'blue'
                    }
                
            else:
                list = { # 出勤 過去
                        'title':str(info.starth) + ":" + str(info.startm) + " ~ " + str(info.endh) + ":" + str(info.endm),
                        'date': info.day,
                        'color': 'blue'
                    }
                
        events.append(list) # 過去のデータ分の出勤記録も表示するためにappend
        
    return render_template('history.html',username=user, events=events)


# Todo
@app.route('/memo/<user>', methods=['GET', 'POST'])
def todo(user):
    
    tasks = Todo.query.filter_by(user=user).order_by(Todo.date_created).all() # Todoリスト取得
    return render_template('memo.html', tasks=tasks, username=user)


# タスク追加
@app.route('/add/<user>', methods=['GET', 'POST'])
def memo(user):
    
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(memo=task_content, user=user)

        try:
            db.session.add(new_task)
            db.session.commit()
            tasks = Todo.query.filter_by(user=user).order_by(Todo.date_created).all()
            return render_template('memo.html',tasks=tasks, username=user)
        
        except:
            return "エラー"
        
    else:
        tasks = Todo.query.filter_by(user=user).order_by(Todo.date_created).all()
        return render_template('memo.html', tasks=tasks, username=user)


# タスク削除
@app.route('/delete/<user>/<int:id>')
def delete(user, id):
    
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        tasks = Todo.query.filter_by(user=user).order_by(Todo.date_created).all()
        return render_template('memo.html', tasks=tasks, username=user)
   
    except:
        return 'エラー'


# 出退勤時間の変更申請
@app.route('/edit/<user>', methods=['GET', 'POST'])
def update(user):
    
    if request.method == 'POST':
        # フォームから取得
        text = request.form.get('content')
        time = request.form.get('time')
        date = request.form.get('date')
        endh = time.split(':', 1)[0] # 分割
        endm = time.split(':', 1)[1] # 分割
        
        # 重複チェック用
        check = Request.query.filter_by(user=user).first()
        
        if check is None:
            new_request = Request(user=user, text=text, date=date, endh=endh, endm=endm)
            db.session.add(new_request)
            db.session.commit()
        
        else:
            pass
        
        requests = Request.query.all()
        return render_template('edit.html', username=user, request=requests)
    
    else:
        requests = Request.query.all()
        return render_template('edit.html', username=user, request=requests)


# 出退勤時間の変更許可
@app.route('/accept/<user>', methods=['GET', 'POST'])
def accept(user):
    
    # ユーザーの申請情報を取得
    requests = Request.query.filter_by(user=user).first()
    endh = requests.endh
    endm = requests.endm
    date = requests.date
    text = requests.text
    
    # ユーザー情報のデータを取得
    now_data = User.query.filter_by(user=user, day=date).first()    
    
    if now_data != None:
    
        # 出勤時間の変更
        if text == "出勤":    
            now_data.starth = endh
            now_data.startm = endm
        
        # 退勤時間の変更
        else:
            now_data.endh = endh
            now_data.endm = endm
        
        db.session.commit()
    
    # 出勤していない状態での出勤申請
    else:
        new_data = User(user=user, day=date, starth=endh, startm=endm) 
        db.session.add(new_data)
        db.session.commit()
    
    # 変更申請の削除
    request_to_delete = Request.query.filter_by(user=user).first()
    db.session.delete(request_to_delete)
    db.session.commit()
        
    return redirect('/edit/Admin')
    

# 出退勤時間の変更拒否
@app.route('/reject/<user>', methods=['GET', 'POST'])
def reject(user):
    
    request_to_delete = Request.query.filter_by(user=user).first()
    db.session.delete(request_to_delete)
    db.session.commit()
    
    return redirect('/edit/Admin')
    

# ゲーム
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