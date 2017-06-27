# -*- coding: UTF-8 -*-

from flask import Flask, render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_moment import Moment
from flask_login import LoginManager
from flaskext.markdown import Markdown


db = SQLAlchemy()
mail = Mail()
moment = Moment()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    mkr = Markdown(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .gem import gem as gem_blueprint
    app.register_blueprint(gem_blueprint)

    from .counsil import counsil as counsil_blueprint
    app.register_blueprint(counsil_blueprint)

    from .draft import draft as draft_blueprint
    app.register_blueprint(draft_blueprint)
    
    from .proposal import proposal as proposal_blueprint
    app.register_blueprint(proposal_blueprint)

    from .gem_stat import gem_stat as gem_stat_blueprint
    app.register_blueprint(gem_stat_blueprint)

    return app
