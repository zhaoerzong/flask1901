import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'   #windows
else:
    prefix = 'sqlite:////'   #linux，mic其他平台




app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'



db = SQLAlchemy(app)  #初始化扩展，传入程序实例app




login_manager = LoginManager(app)  #实例化扩展类
@login_manager.user_loader
def load_user(user_id):
    from blog.models import User
    user = User.query.get(int(user_id))
    return user
login_manager.login_view = 'login'
login_manager.login_message = '您未登录!'




#模板上下文处理函数,在多个模板内都需要使用的变量
@app.context_processor
def inject_user():
    from blog.models import User
    user = User.query.first()
    return dict(user=user)




from blog import views,errors,commands