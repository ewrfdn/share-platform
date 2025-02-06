from .base import database, BaseModel
from .user import User
from .role import Role
from .category import Category
from .blob import Blob
from .material import Material
from .comment import Comment

# 所有模型列表,用于创建表
MODELS = [User, Role, Category, Blob, Material, Comment]

def init_db(app):
    """初始化数据库连接"""
    database.init(
        app.config['DB_NAME'],
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD']
    )
    
    # 创建表
    database.connect()
    database.create_tables(MODELS)
    database.close() 