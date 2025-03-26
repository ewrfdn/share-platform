from flask import Blueprint, jsonify
from app.services.role_service import RoleService
from app.utils.jwt import jwt_required

role_bp = Blueprint('role', __name__)

@role_bp.route('/roles', methods=['GET'])
@jwt_required(allowed_roles=[1, 2])  # Admins and teachers can view roles
def get_roles():
    roles = RoleService.get_all_roles()
    roles = [ role.to_json() for role in roles]
    return jsonify(roles), 200
