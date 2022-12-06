from flask import Flask, render_template
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
import toml

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '21b2d14b80016e3cf3bc8ea9302cd332b45732ad'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
    # app.config['SQLALCHEMY_DATABASE_URI'] = " postgres://fgbtejvdoaedpd:e40bbfc52e90adf0be4fe382ed93d7788125ee933d125c618d57237fc177aa3d@ec2-3-227-68-43.compute-1.amazonaws.com:5432/d8f0eu0p51ndju"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_file("config.toml", load=toml.load)
    app.config.from_object('alumni.default_settings')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS')
    ckeditor = CKEditor(app)
    from alumni.models import User, Members, Blogs, Profile
    from alumni.auth import auth
    from alumni.views import views
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')


    @app.errorhandler(500)
    def internalerror(e):
        return render_template('500.html')
        
    db.init_app(app)
    migrate.init_app(app, db)

    return app




# def create_database(app):
#     if not path.exists('alumni/' + database):
#         db.create_all(app=app)
#         print("Creaed Database!")


