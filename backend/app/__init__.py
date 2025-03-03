from flask import Flask, make_response, jsonify
from flask_cors import CORS
from app.config import Config
from app.routes.blob import blob_bp
from app.routes.user import user_bp
from app.routes.auth import auth_bp
from .routes.role import role_bp

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configure JSON responses to use UTF-8
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json; charset=utf-8"
    app.config['JSON_SORT_KEYS'] = False
    
    # Enhanced JSON response handling
    @app.after_request
    def after_request(response):
        if response.mimetype == "application/json":
            response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    
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
    app.register_blueprint(role_bp, url_prefix='/api')
    
    return app