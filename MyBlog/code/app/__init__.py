from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_moment import Moment
from config import Config


db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()
'''
开启会话保护后，每一个请求会根据访问的IP地址和用户代理（User Agent）生成一个识别码。在strong模式下，如果请求的识别码不同就会直接删除会话（所以需要重新登录）。
'''
# login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    # app = Flask(__name__,static_url_path='/myblog')
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    CsrfProtect(app)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
