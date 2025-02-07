import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from app.config import Config
from app.models.user import User
from typing import List, Optional

def create_access_token(identity: int) -> str:
    """
    创建访问令牌
    :param identity: 用户ID
    :return: JWT token字符串
    """
    # 获取用户角色信息
    user = User.get_or_none(User.id == identity)
    if not user:
        raise ValueError('用户不存在')
        
    payload = {
        'user_id': identity,
        'role_id': user.role_id,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def jwt_required(allowed_roles: Optional[List[int]] = None):
    """
    JWT认证装饰器
    :param allowed_roles: 允许访问的角色ID列表，为None时表示允许所有角色访问
    """
    def jwd_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': '缺少认证token'}), 401
                
            try:
                token = token.split(' ')[1]
                payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
                
                # 将用户信息存储到request中
                request.user_id = payload['user_id']
                request.role_id = payload['role_id']
                
                # 如果指定了允许的角色，则进行权限检查
                if allowed_roles is not None and payload['role_id'] not in allowed_roles:
                    return jsonify({
                        'message': '权限不足',
                        'required_roles': allowed_roles,
                        'current_role': payload['role_id']
                    }), 403
                    
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'token已过期'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': '无效的token'}), 401
                
            return fn(*args, **kwargs)
        return wrapper
    return jwd_decorator 