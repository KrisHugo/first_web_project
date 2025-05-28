
from flask import Flask
from .config import Config
from .extensions import db, bcrypt, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # # 注册蓝图
    # from .routes.auth import auth_bp
    # from .routes.user import user_bp
    # app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # app.register_blueprint(user_bp, url_prefix='/api/users')

    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .routes import init_routes
    init_routes(app, jwt)

    # 导入并注册蓝图等
    # from . import models
    with app.app_context():
        db.create_all()
    
    return app