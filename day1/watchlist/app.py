import os
import sys
import click

from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy   #导入扩展类

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'   #windows
else:
    prefix = 'sqlite:////'   #linux，mic其他平台


app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)  #初始化扩展，传入程序实例app


#自定义命令
@app.cli.command()    #装饰器，注册命令
@click.option('--drop',is_flag=True,help='Create after drop(删除后再创建)')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库完成。。。')


#models
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)  #主键
    name = db.Column(db.String(20))   #名字

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)   #主键
    title = db.Column(db.String(60))  #电影标题
    year = db.Column(db.String(4))  #电影年份


@app.cli.command()
def forge():
    db.create_all()
    name = "聪"
    movies = [
        {'title':'功夫之王','year':'2010'},
        {'title':'机器之血','year':'2015'},
        {'title':'复仇者联盟3','year':'2017'},
        {'title':'微微一笑很倾城','year':'2018'},
        {'title':'百鸟朝凤','year':'2019'},
        {'title':'唐人街探案3','year':'2020'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('导入数据完成')


#views
#多URL

@app.route('/',methods=['GET','POST'])
# @app.route('/index')
# @app.route('/home')


#首页
def index():

    # user = User.query.first()   #读取用户记录
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        #验证数据不为空，year长度不能超过4，title长度不能超过60
        if not title or not year or len(year)>4 or len(title)>60:
            flash('输入错误！！')
            return redirect(url_for('index'))
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('电影数据已添加成功！！！')
        return redirect(url_for('index'))

    movies = Movie.query.all()  #读取所有电影记录
    return render_template('index.html',movies=movies)
    # return "<h1>hello,Flask!!!</h1>"



#编辑电影信息视图函数
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(title)>60 or len(year)>4:
            flash('请正确输入编辑电影信息')
            return redirect(url_for('edit'),movie_id=movie_id)

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('电影信息编辑成功')
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)
    



#删除电影信息
@app.route('/movie/delete/<int:movie_id>',methods=['GET','POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除数据成功')
    return redirect(url_for('index'))


#处理页面404错误
@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first()
    return render_template('404.html'),404



#模板上下文处理函数,在多个模板内都需要使用的变量
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)





#动态URL
# @app.route('/index/<name>')
# def home(name):
#     print(url_for("home",name='Cong'))
#     return "<h1>hello,%s!!!</h1>"%name