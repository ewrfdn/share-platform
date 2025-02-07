from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes.blob import blob_bp
from app.routes.user import user_bp
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    
    # 配置JSON编码（Flask 2.0.1 版本的正确设置方式）
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json; charset=utf-8"
    app.config['JSON_SORT_KEYS'] = False
    
    # 加载其他配置
    app.config.from_object(Config)
    
    # 配置CORS
    CORS(app)
    
    # 服务检测
    @app.route('/', methods=['GET'])
    def health():
        return 'OK'
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(blob_bp, url_prefix='/api/blob')
    app.register_blueprint(user_bp, url_prefix='/api/admin')
    
    return app 