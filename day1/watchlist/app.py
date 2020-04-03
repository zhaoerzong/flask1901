import os
import sys
import click

from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy   #导入扩展类
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user

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

login_manager = LoginManager(app)  #实例化扩展类
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'
login_manager.login_message = '您未登录!'






#models
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)  #主键
    name = db.Column(db.String(20))   #名字
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)   #主键
    title = db.Column(db.String(60))  #电影标题
    year = db.Column(db.String(4))  #电影年份


#自定义命令（初始化数据库）
@app.cli.command()    #装饰器，注册命令
@click.option('--drop',is_flag=True,help='Create after drop(删除后再创建)')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库完成。。。')


#导入数据指令
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



#生成管理员账户
@app.cli.command()
@click.option('--username',prompt=True,help='用户名')
@click.option('--password',prompt=True,help='密码',confirmation_prompt=True)
def admin(username,password):
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('更新用户信息')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建新用户')
        user = User(username=username,name='聪')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('管理员创建完成')




#多URL
@app.route('/',methods=['GET','POST'])
# @app.route('/index')
# @app.route('/home')


#首页
def index():

    # user = User.query.first()   #读取用户记录
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        #request在请求触发的时候才会包含数据
        title = request.form.get('title')
        year = request.form.get('year')
        #验证数据不为空，year长度不能超过4，title长度不能超过60
        if not title or not year or len(year)>4 or len(title)>60:
            flash('输入错误！！')
            return redirect(url_for('index'))
        #保存表单数据
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
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year)>4 or len(title)>60:
            flash('不能为空或超过最大长度')
            return redirect(url_for('index'))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('电影信息编辑完成')
        return redirect(url_for('index'))

    return render_template('edit.html',movie=movie)
    



#删除电影信息
@app.route('/movie/delete/<int:movie_id>',methods=['GET','POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除数据成功')
    return redirect(url_for('index'))


#登录页面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('账号或密码输入错误')
            return redirect(url_for('login'))
        
        user = User.query.first()
        #验证用户名和密码是否和数据库的一致
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功！！')
            return redirect(url_for('index'))
        flash('用户名或密码错误')
        return redirect(url_for('login'))
    return render_template('login.html')



#退出页面
@app.route('/logout')
def logout():
    logout_user()
    flash('退出成功~')
    return redirect(url_for('index'))





#设置name页面
@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name)>20:
            flash('输入非法,请正确输入！！')
            return redirect(url_for('settings'))
        current_user.name = name
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('name设置成功！')
        return redirect(url_for('index'))
    return render_template('settings.html')


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