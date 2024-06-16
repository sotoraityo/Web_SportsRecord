from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date,timedelta,time
import pandas as pd
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy import desc,asc
import os
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash

import os
import csv
import urllib.request
from bs4 import BeautifulSoup

from scraping import str2float,scraping,create_csv



#%%
#flaskクラスのインスタンス作成
app = Flask(__name__)
#データベースの作成
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "sotoraityo",
      'password': "Pass4321",
      'host': "sotoraityo.mysql.pythonanywhere-services.com",
      'db_name': "sotoraityo$webdb"
  })
app.config['SECRET_KEY'] = os.urandom(24)
#dbの設定
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["REMEMBER_COOKIE_DURATION"]=timedelta(hours=20)

db = SQLAlchemy(app)

#%%
#ログインのクラス作成
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"ログインをしてください"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#%%
#アカウントのDB
class User(UserMixin,db.Model):
    #__tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),nullable=False,unique=True)
    password=db.Column(db.String(20),nullable=False)

#投稿内容のDB
class Post(db.Model):
    #__tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=True)
    health=db.Column(db.String(20), nullable=True)
    healthdetail=db.Column(db.String(30), nullable=True)

    weight=db.Column(db.Integer,nullable=True)
    breakf = db.Column(db.String(20), nullable=True)
    lunch = db.Column(db.String(20), nullable=True)
    dinner = db.Column(db.String(20), nullable=True)
    breakfTime = db.Column(db.Time, nullable=True)
    lunchTime = db.Column(db.Time, nullable=True)
    dinnerTime = db.Column(db.Time, nullable=True)

    detail = db.Column(db.Text, nullable=True)
    post_date = db.Column(db.DateTime, nullable=True)

    wake_temp=db.Column(db.REAL,nullable=True)
    before_temp=db.Column(db.REAL,nullable=True)
    warm_temp=db.Column(db.REAL,nullable=True)
    after_temp=db.Column(db.REAL,nullable=True)
    bed_temp=db.Column(db.REAL,nullable=True)
    sihyovalue1=db.Column(db.Integer,nullable=True)
    sihyovalue2=db.Column(db.Integer,nullable=True)
    sihyovalue3=db.Column(db.Integer,nullable=True)
    sihyovalue4=db.Column(db.Integer,nullable=True)
    sihyovalue5=db.Column(db.Integer,nullable=True)

    menu=db.Column(db.Text,nullable=True)
    menuStart=db.Column(db.Time,nullable=True)
    menuEnd=db.Column(db.Time,nullable=True)

    thred = db.Column(db.Integer, nullable=True)

#練習内容のDB
class Trainingmenu(UserMixin,db.Model):
    #__tablename__ = 'trainingmenu'
    id=db.Column(db.Integer,primary_key=True)
    schoolcode=db.Column(db.Integer,nullable=False)
    menuName = db.Column(db.String(20), nullable=True)
    menuLevel=db.Column(db.Integer, nullable=True)
    menuTime=db.Column(db.Integer, nullable=True)
    menuMemo=db.Column(db.Text,nullable=True)

#練習セットのDB
class Trainingset(UserMixin,db.Model):
    #__tablename__ = 'trainingset'
    id=db.Column(db.Integer,primary_key=True)
    setName = db.Column(db.String(20), nullable=True)
    setMemo=db.Column(db.Text,nullable=True)

#練習セット内容のDB
class Setmenu(UserMixin,db.Model):
    #__tablename__ = 'setmenu'
    id=db.Column(db.Integer,primary_key=True)
    setmenuName = db.Column(db.String(20), nullable=True)
    setmenuStart=db.Column(db.Time,nullable=True)
    setmenuTime=db.Column(db.Integer,nullable=True)
    setmenuMemo=db.Column(db.Text,nullable=True)
    setId=db.Column(db.Integer,nullable=True)

#%%
#メインページ
#
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # 今日の記録の確認
    dt_today =date.today().strftime("%Y-%m-%d")
    dt_today=dt_today+" 00:00:00"
    todaytime=datetime.strptime(dt_today,"%Y-%m-%d %H:%M:%S")

    check="記録済み"

    #記録がないか確認
    filter = Post.query.filter_by(user=current_user.username,post_date=todaytime).first()
    if filter==None:
        check="未記録"

    return render_template('home.html',username=current_user.username,
                            check=check)

#%%
#新規登録サインアップページ
#
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userのインスタンスを作成（セキュリティのためハッシュ化する）
        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()
        return redirect('/signup')
    else:
        return render_template('signup.html')



#%%
#ログインページ
#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        #user名がない時
        if user==None:
            flash("そのユーザーは存在しません", "failed")
            return redirect('/login')

        # パスワードの確認
        else:
            if user.password==password:
                login_user(user)
                return redirect('/')
            else:
                flash("パスワードが異なります", "failed")

        return redirect('/login')

    else:
        return render_template('login.html')


#%%
#ログアウトページ
#
@app.route('/logout')
@login_required
def logout():
    #ユーザーをログアウトさせる
    logout_user()
    return redirect('/login')


#%%
#目次ページ
#
@app.route('/index')
def index():
    #Postデータベースからすべての投稿を取り出す
    db.session.commit()
    posts=Post.query.order_by(desc(Post.post_date)).filter(Post.thred==0,
            Post.user==current_user.username)
    return render_template('index.html', posts=posts)


#%%
#記録作成ページ
#
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method=="POST":
        #練習メニュー、セットをDBから取得
        menus=Trainingmenu.query.all()
        sets=Trainingset.query.all()
        #データを取得、date型に変換する
        select_date=request.form.get('select_date')
        select_date= datetime.strptime(select_date, "%Y-%m-%d")
        #Noneなら今日の日付を返す
        if select_date==None:
            select_date=datetime.now()

        #日付が既にあるか確認
        posts=Post.query.filter(Post.post_date==select_date,Post.thred==0,Post.user==current_user.username)
        check=posts.count()
        if check!=0:
            #既にあるなら詳細ページに移行
            id=posts[0].id
            return redirect('/arrange/'+str(id))

        #無いなら投稿作成に移行
        return render_template('create.html',datenow=select_date,username=current_user.username,menus=menus,sets=sets)
    else:
        dt_now =datetime.now()
        menus=Trainingmenu.query.all()
        sets=Trainingset.query.all()
        return render_template('create.html',datenow=dt_now,username=current_user.username,menus=menus,sets=sets)


#%%
#投稿作成完了url
#
@app.route('/createupload', methods=['GET', 'POST'])
@login_required
def main():
    if request.method=='GET':
        return redirect('/calendar')

    #Postのデータを読み取り、postdataにデータを保存し、newpostを作る
    else:
        #日付が既にあるか確認
        get_date = request.form.get("post_date","2023-10-10")# formから取得
        post_date = datetime.strptime(get_date, "%Y-%m-%d")
        posts=Post.query.filter(Post.post_date==post_date,Post.user==current_user.username)# DBを確認

        #既にあるなら本当にするか確認
        if  posts.count():
            flash("既にありました", "failed")
            return render_template('create.html',datenow=post_date)


        #フォームからデータの入力、仮の初期値
        user = current_user.username
        health=request.form.get('health',"good")
        weight=request.form.get('weight',"00")
        breakf = request.form.get('breakf',"なし")
        lunch=request.form.get('lunch',"なし")
        dinner=request.form.get('dinner',"なし")
        breakfTime=request.form.get('breakfTime',"")
        lunchTime=request.form.get('lunchTime',"")
        dinnerTime=request.form.get('dinnerTime',"")

        detail = request.form.get('detail',"なし")
        post_date = request.form.get("post_date","2021-12-31")

        wake_temp= request.form.get('wake_temp',"35.0")
        before_temp= request.form.get('before_temp',"35.1")
        warm_temp= request.form.get('warm_temp',"35.2")
        after_temp= request.form.get('after_temp',"35.3")
        bed_temp= request.form.get('bed_temp',"35.4")
        sihyovalue1= request.form.get('sihyo1',"0")
        sihyovalue2= request.form.get('sihyo2',"0")
        sihyovalue3= request.form.get('sihyo3',"0")
        sihyovalue4= request.form.get('sihyo4',"0")
        sihyovalue5= request.form.get('sihyo5',"0")
        thred=0

        menus = request.form.getlist('menucheck')
        menu=",".join(menus)
        menuStart=request.form.get('menuStart',"16:30")
        menuEnd=request.form.get('menuEnd',"18:00")

        healthcheck = request.form.getlist('healthcheck')
        healthdetail=",".join(healthcheck)

        #文字列から日付型に変換(date)
        post_date = datetime.strptime(post_date, "%Y-%m-%d")
        #time型に変換
        timeformat="%H:%M"
        breakfTime=datetime.strptime(breakfTime,timeformat)
        lunchTime=datetime.strptime(lunchTime,timeformat)
        dinnerTime=datetime.strptime(dinnerTime,timeformat)
        #メニュー開始、終了
        menuStart=datetime.strptime(menuStart,timeformat)
        menuEnd=datetime.strptime(menuEnd,timeformat)


        new_post = Post(user=user, breakf=breakf,lunch=lunch,dinner=dinner,
                        breakfTime=breakfTime,lunchTime=lunchTime,dinnerTime=dinnerTime,
                        health=health,healthdetail=healthdetail,weight=weight,
                        detail=detail,post_date=post_date,
                        wake_temp=wake_temp,before_temp=before_temp,
                        warm_temp=warm_temp,after_temp=after_temp,
                        bed_temp=bed_temp,
                        sihyovalue1=sihyovalue1,sihyovalue2=sihyovalue2,
                        sihyovalue3=sihyovalue3,sihyovalue4=sihyovalue4,
                        sihyovalue5=sihyovalue5,
                        menu=menu,menuStart=menuStart,menuEnd=menuEnd,
                        thred=thred)

        db.session.add(new_post)
        db.session.commit()

        #if post_date.strftime("%Y-%m-%d")!=date.today().strftime("%Y-%m-%d"):
        #    create_csv(post_date)
        return redirect('/calendar')


#%%
#詳細ページ　データベースのIDからデータを指定
#
@app.route('/detail/<int:id>')
@login_required
def detail(id):
    #idの指定
    post = Post.query.get(id)
    comments=Post.query.filter(Post.thred==id)
    dt_now =datetime.now()
    return render_template('detail.html', post=post,comments=comments,datenow=dt_now)

#%%
#編集ページ
#
@app.route('/arrange/<int:id>',methods=['GET', 'POST'])
@login_required
def arrange(id):
    #idのポストを取得
    post = Post.query.get(id)
    return render_template('createArra.html', post=post,username=current_user.username)

#%%
#削除ページ
#
@app.route('/delete/<int:id>',methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/calendar')

#%%
#コメントページ
#
@app.route('/comment/<int:id>',methods=['GET', 'POST'])
@login_required
def comment(id):
    user = request.form.get('user',"nanasi")
    health=request.form.get('health',"good")
    weight=request.form.get('weight',"00")
    breakf = request.form.get('breakf',"今日の朝食")
    lunch=request.form.get('lunch',"今日の朝食")
    dinner=request.form.get('dinner',"今日の朝食")
    detail = request.form.get('detail',"ヤマザキパン")
    post_date = request.form.get("post_date","2021-12-31")

    #文字列から日付型に変換(date)
    post_date = datetime.strptime(post_date, "%Y-%m-%d")
    new_post = Post(user=user, breakf=breakf,lunch=lunch,dinner=dinner,
                    health=health,weight=weight,
                    detail=detail,post_date=post_date,thred=id)

    db.session.add(new_post)
    db.session.commit()
    return redirect('/detail/'+str(id))


#%%
#編集完了ページ
#
@app.route('/arrangeFin/<int:id>',methods=['GET', 'POST'])
@login_required
def arrangeFin(id):
    post = Post.query.get(id)

    #フォームからデータの入力、仮の初期値
    user = current_user.username
    health=request.form.get('health',"good")
    weight=request.form.get('weight',"00")
    breakf = request.form.get('breakf',"なし")
    lunch=request.form.get('lunch',"なし")
    dinner=request.form.get('dinner',"なし")
    breakfTime=request.form.get('breakfTime',"")
    lunchTime=request.form.get('lunchTime',"")
    dinnerTime=request.form.get('dinnerTime',"")

    detail = request.form.get('detail',"なし")
    post_date = request.form.get("post_date","2021-12-31")

    wake_temp= request.form.get('wake_temp',"35.0")
    before_temp= request.form.get('before_temp',"35.1")
    warm_temp= request.form.get('warm_temp',"35.2")
    after_temp= request.form.get('after_temp',"35.3")
    bed_temp= request.form.get('bed_temp',"35.4")
    sihyovalue1= request.form.get('sihyo1',"0")
    sihyovalue2= request.form.get('sihyo2',"0")
    sihyovalue3= request.form.get('sihyo3',"0")
    sihyovalue4= request.form.get('sihyo4',"0")
    sihyovalue5= request.form.get('sihyo5',"0")

    menus = request.form.getlist('menucheck')
    menu=",".join(menus)
    menuStart=request.form.get('menuStart',"16:30")
    menuEnd=request.form.get('menuEnd',"18:00")

    healthcheck = request.form.getlist('healthcheck')
    healthdetail=",".join(healthcheck)

    #文字列から日付型に変換(date)
    post_date = datetime.strptime(post_date, "%Y-%m-%d")
    #time型に変換
    timeformat="%H:%M:%S"
    breakfTime=datetime.strptime(breakfTime,timeformat)
    lunchTime=datetime.strptime(lunchTime,timeformat)
    dinnerTime=datetime.strptime(dinnerTime,timeformat)
    #メニュー開始、終了
    menuStart=datetime.strptime(menuStart,timeformat)
    menuEnd=datetime.strptime(menuEnd,timeformat)


    post.user=user
    post.health=health
    post.weight=weight
    post.breakf=breakf
    post.lunch=lunch
    post.dinner=dinner
    post.detail=detail
    post.post_date=post_date
    post.user=user

    post.healthdetail=healthdetail

    post.health=health
    post.wake_temp=wake_temp
    post.before_temp=before_temp
    post.warm_temp=warm_temp
    post.after_temp=after_temp
    post.bed_temp=bed_temp
    post.sihyovalue1= sihyovalue1
    post.sihyovalue2= sihyovalue2
    post.sihyovalue3= sihyovalue3
    post.sihyovalue4= sihyovalue4
    post.sihyovalue5= sihyovalue5

    post.menu=menu
    post.menuStart=menuStart
    post.menuEnd=menuEnd


    db.session.commit()
    return redirect('/index')

#%%
#カレンダーのページ
#
@app.route('/calendar',methods=['GET','POST'])
@login_required
def calender():
    #投稿してある日付を取得、htmlにわたす
    db.session.commit()
    post_dates=Post.query.filter(Post.thred==0,Post.user==current_user.username)
    return render_template('calendar.html', post_dates=post_dates)

#
#メニュー一覧
#
@app.route('/setmenu', methods=['GET', 'POST'])
@login_required
def menuup():
    #Trainingmenuデータベースから全てのデータを取り出す
    db.session.commit()
    menus=Trainingmenu.query.all()
    sets=Trainingset.query.all()
    setmenus=Setmenu.query.order_by(asc(Setmenu.setmenuStart)).all()

    return render_template('setmenu.html',menus=menus,sets=sets,setmenus=setmenus)

#
#メニュー作成（作成後一覧にリダイレクト）
#
@app.route('/menuCreate', methods=['GET', 'POST'])
@login_required
def menuCreate():
    if request.method == "POST":
        schoolcode=request.form.get('schoolcode',"0")
        menuName =request.form.get('menuName','オリジナル')
        menuLevel=request.form.get('menuLevel',"5")
        menuTime=request.form.get('menuTime',"30")
        menuMemo=request.form.get('menuMemo',"なし")
        if menuMemo=="":
            menuMemo="なし"
        #メニューのインスタンス作成
        menu = Trainingmenu(schoolcode=schoolcode, menuName=menuName,menuLevel=menuLevel,
                            menuTime=menuTime,menuMemo=menuMemo)

        db.session.add(menu)
        db.session.commit()
        return redirect('/setmenu')
    else:
        return redirect('/setmenu')


#
#セット作成（作成後一覧にリダイレクト）
#
@app.route('/setCreate', methods=['GET', 'POST'])
@login_required
def setCreate():
    if request.method == "POST":
        ##セットの枠作成
        setName = request.form.get("setName")
        setMemo=request.form.get("setMemo",'なし')
        if setMemo=="":
            setMemo="なし"

        #メニューのインスタンス作成
        trainingset = Trainingset(setName=setName, setMemo=setMemo)
        db.session.add(trainingset)
        db.session.commit()

        ##セットメニューの内容作成
        setmenuNames = request.form.getlist("setmenuName")
        setmenuStarts = request.form.getlist("setmenuStart")

        for (setmenuName,setmenuStart) in zip(setmenuNames,setmenuStarts):
            if setmenuName!=None:
                setmenuStart=datetime.strptime(setmenuStart, "%H:%M")
                #メニューを取り出し時間を取得
                menuTarget=Trainingmenu.query.filter(Trainingmenu.menuName==setmenuName).first()
                if menuTarget==None:
                    break
                setmenuTime=menuTarget.menuTime
                setmenuMemo=menuTarget.menuMemo
                #セットの参照Id
                setId=trainingset.id

                setmenu=Setmenu(setmenuName=setmenuName,setmenuStart=setmenuStart,
                                setId=setId,setmenuTime=setmenuTime,
                                setmenuMemo=setmenuMemo)
                db.session.add(setmenu)

        db.session.commit()
        return redirect('/setmenu')
    else:
        return redirect('/setmenu')


#%%
#メニュー削除ページ
#
@app.route('/deletemenu/<int:id>',methods=['GET', 'POST'])
@login_required
def deleteMenu(id):
    menu = Trainingmenu.query.get(id)
    db.session.delete(menu)
    db.session.commit()
    return redirect('/setmenu')

#%%
#セット削除ページ
#
@app.route('/deleteset/<int:id>',methods=['GET', 'POST'])
@login_required
def deleteSet(id):
    set = Trainingset.query.get(id)
    db.session.delete(set)
    db.session.commit()
    return redirect('/setmenu')

#%%
#管理者リストページ
#
@app.route('/admin_list', methods=['GET', 'POST'])
def admin_list():
    #管理者以外のユーザーを渡す
    db.session.commit()
    #users=User.query.filter(User.username!=current_user.username)
    users=User.query.filter(User.username!="admin")

    # 今日の記録の確認
    dt_today =date.today().strftime("%Y-%m-%d")
    dt_today=dt_today+" 00:00:00"
    todaytime=datetime.strptime(dt_today,"%Y-%m-%d %H:%M:%S")
    checks=[]

    for user in users:
        check="記録済み"
        #記録がないか確認
        filter = Post.query.filter_by(user=user.username,post_date=todaytime).first()
        if filter==None:
            check="未記録"

        checks.append(check)

    return render_template('admin_list.html',users=users,checks=checks)


#%%
#管理者ユーザー詳細ページ
#
@app.route('/admin_user/<int:id>', methods=['GET', 'POST'])
def admin_user(id):
    #ユーザーの情報を取得
    db.session.commit()
    user=User.query.get(id)
    #投稿日を取得
    post_dates=Post.query.filter(Post.thred==0, Post.user==user.username)
    return render_template('admin_user.html', post_dates=post_dates,user=user)


#%%
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

