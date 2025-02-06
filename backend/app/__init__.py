from flask import Flask
from flask_cors import CORS
from peewee import MySQLDatabase
from config import Config
from .routes.blob import blob_bp
from .routes.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 配置CORS
    CORS(app)
    
    # 配置数据库
    db = MySQLDatabase(
        Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    
    # 注册蓝图
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # 注册blob蓝图
    app.register_blueprint(blob_bp, url_prefix='/api/blobs')
    
    # 注册user蓝图
    app.register_blueprint(user_bp, url_prefix='/api')
    
    return app 