import os
import sys
import click

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy   #导入扩展类

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'   #windows
else:
    prefix = 'sqlite:////'   #linux，mic其他平台


app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #关闭对模型修改的监控
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




#views
#多URL
@app.route('/')
# @app.route('/index')
# @app.route('/home')

def index():
    # name = "大聪"
    # movies = [
    #     {'title':'杀破狼','year':'2010'},
    #     {'title':'唐人街探案','year':'2015'},
    #     {'title':'战狼2','year':'2017'},
    #     {'title':'我不是药神','year':'2018'},
    #     {'title':'复仇者联盟4','year':'2019'},
    #     {'title':'大赢家','year':'2020'},
    # ]
    user = User.query.first()   #读取用户记录
    movies = Movie.query.all()  #读取所有电影记录
    return render_template('index.html',user=user,movies=movies)
    # return "<h1>hello,Flask!!!</h1>"


#动态URL
# @app.route('/index/<name>')
# def home(name):
#     print(url_for("home",name='Cong'))
#     return "<h1>hello,%s!!!</h1>"%name