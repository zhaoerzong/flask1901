from flask import redirect,render_template,flash,request

from blog import db,app
from blog.models import User,Movie

from flask_login import LoginManager,login_required,current_user,login_user,logout_user




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