from flask import Flask,render_template
app = Flask(__name__)


#多URL
@app.route('/')
# @app.route('/index')
# @app.route('/home')

def index():
    name = "大聪"
    movies = [
        {'title':'杀破狼','year':'2010'},
        {'title':'唐人街探案','year':'2015'},
        {'title':'战狼2','year':'2017'},
        {'title':'我不是药神','year':'2018'},
        {'title':'复仇者联盟4','year':'2019'},
        {'title':'大赢家','year':'2020'},
    ]
    return render_template('index.html',name=name,movies=movies)
    # return "<h1>hello,Flask!!!</h1>"


#动态URL
# @app.route('/index/<name>')
# def home(name):
#     print(url_for("home",name='Cong'))
#     return "<h1>hello,%s!!!</h1>"%name