from flask import Flask, make_response, jsonify
from flask_cors import CORS
from app.config import Config
from app.routers.auth import auth_bp
from app.routers.role import role_bp
from app.routers.user import user_bp
from app.routers.category import category_bp
from app.routers.material import material_bp
from app.routers.blob import blob_bp
import orjson


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
    
    # 配置上传文件夹
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    # 使用 orjson 进行 JSON 序列化
    # 服务检测
    @app.route('/', methods=['GET'])
    def health():
        return 'OK'
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(role_bp, url_prefix='/api/role')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(category_bp, url_prefix='/api/category')
    app.register_blueprint(material_bp, url_prefix='/api/material')
    app.register_blueprint(blob_bp, url_prefix='/api/blob')
    
    return app