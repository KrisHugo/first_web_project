import os
from flask_cors import CORS  # 解决跨域问题
# from backend import create_app
from app import create_app
# MySQL 配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "test_db",
    # "cursorclass": pymysql.cursors.DictCursor  # 返回字典格式数据
}


# def create_app(config=None):
#     app = Flask(__name__)
    
#     # 统一使用 SQLAlchemy 配置
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/test_db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     # JWT 配置
#     app.config["JWT_SECRET_KEY"] = "123456789abc"  # 生产环境要用更复杂的密钥
#     app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

#     # 配置应用
#     if config is not None:
#         app.config.from_object(config)
    
#     # 初始化扩展
#     db.init_app(app)
#     bcrypt.init_app(app)
#     jwt.init_app(app)

    

#     # 导入并注册蓝图等
#     # from . import models
#     with app.app_context():
#         db.create_all()
    
#     return app

app = create_app()
if __name__ == '__main__':
    CORS(app)  # 允许所有域名跨域访问（生产环境需限制）
    app.run(debug=True, port=5000)