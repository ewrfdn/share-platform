from flask import Blueprint, request, jsonify
from ..services.user_service import UserService, RoleService
from ..utils.jwt import jwt_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@jwt_required(allowed_roles=[1, 2])  # 管理员和老师可以查看
def get_users():
    users = UserService.get_all_users()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'role_id': user.role_id,
        'avatar': user.avatar,
        'created_at': user.created_at.isoformat(),
    } for user in users]), 200

@user_bp.route('/users', methods=['POST'])
@jwt_required(allowed_roles=[1, 2])  # 管理员和老师可以创建
def create_user():
    data = request.get_json()
    
    if not all(k in data for k in ('username', 'password', 'role_id')):
        return jsonify({'message': '缺少必要的字段'}), 400

    try:
        user = UserService.create_user(
            username=data['username'],
            password=data['password'],
            role_id=data['role_id'],
            current_user_role_id=request.role_id
        )
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role_id': user.role_id,
            'created_at': user.created_at.isoformat()
        }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required(allowed_roles=[1, 2])  # 管理员和老师可以删除
def delete_user(user_id):
    try:
        if UserService.delete_user(user_id, request.role_id):
            return jsonify({'message': '用户删除成功'}), 200
        return jsonify({'message': '用户不存在'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@user_bp.route('/roles', methods=['GET'])
@jwt_required(allowed_roles=[1])  # 只有管理员可以查看所有角色
def get_roles():
    roles = RoleService.get_all_roles()
    return jsonify([{
        'id': role.id,
        'display_name': role.display_name,
    } for role in roles]), 200 