from blog.models import User,Movie
import click
from blog import app,db



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