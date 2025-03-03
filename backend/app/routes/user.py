from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.utils.jwt import jwt_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@jwt_required(allowed_roles=[1, 2])  # Admins and teachers can view
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
@jwt_required(allowed_roles=[1, 2])  # Admins and teachers can create
def create_user():
    data = request.get_json()
    
    if not all(k in data for k in ('username', 'password', 'role_id')):
        return jsonify({'message': 'Missing required fields'}), 400

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
@jwt_required(allowed_roles=[1, 2])  # Admins and teachers can delete
def delete_user(user_id):
    try:
        # Pass the current user's ID as well
        if UserService.delete_user(user_id, request.role_id, request.user_id):
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'message': 'User does not exist'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required(allowed_roles=[1, 2])  # Admins and teachers can update user
def update_user(user_id):
    data = request.get_json()
    
    try:
        user = UserService.update_user(
            user_id=user_id,
            username=data.get('username'),
            password=data.get('password'),  # May be empty, indicating no password update
            role_id=data.get('role_id'),
            avatar=data.get('avatar'),
            current_user_role_id=request.role_id
        )
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role_id': user.role_id,
            'avatar': user.avatar,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400