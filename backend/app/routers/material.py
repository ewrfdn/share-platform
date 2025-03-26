from flask import Blueprint, request, jsonify
from app.services.material import MaterialService
from app.utils.jwt import jwt_required
from app.exceptions.customer_exceptions import ValidationException, NotFoundException
import orjson

material_bp = Blueprint('material', __name__)

@material_bp.route('/materials', methods=['GET'])
@jwt_required()
def get_materials():
    """获取教材列表，支持分页和过滤"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        display_name = request.args.get('display_name')
        description = request.args.get('description')
        category_ids = request.args.get('category_ids')
        type = request.args.get('type')

        result = MaterialService.get_materials(
            page=page,
            page_size=page_size,
            display_name=display_name,
            description=description,
            category_ids=category_ids,
            type=type
        )
        
        # 使用 orjson 序列化
        return orjson.dumps(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return orjson.dumps({'message': str(e)}), 500, {'Content-Type': 'application/json'}

@material_bp.route('/materials', methods=['POST'])
@jwt_required(allowed_roles=[1, 2])  # 管理员和教师可访问
def create_material():
    """创建教材"""
    try:
        # 从表单数据中获取基本字段
        data = {
            'display_name': request.form.get('display_name'),
            'category_ids': request.form.get('category_ids'),
            'description': request.form.get('description'),
            'cover': request.form.get('cover'),
            'type': request.form.get('type')
        }
        
        # 验证必填字段
        if not all([data['display_name'], data['category_ids'], data['type']]):
            return orjson.dumps({'message': 'Missing required fields'}), 400, {'Content-Type': 'application/json'}
            
        material = MaterialService.create_material(data, request.user_id)
        response = {
            'id': material.id,
            'display_name': material.display_name,
            'category_ids': material.category_ids,
            'type': material.type,
            'created_at': material.created_at.isoformat()
        }
        return orjson.dumps(response), 201, {'Content-Type': 'application/json'}
    except ValidationException as e:
        return orjson.dumps({'message': str(e)}), 400, {'Content-Type': 'application/json'}
    except Exception as e:
        return orjson.dumps({'message': str(e)}), 500, {'Content-Type': 'application/json'}

@material_bp.route('/materials/<int:material_id>', methods=['PUT'])
@jwt_required(allowed_roles=[1, 2])  # 管理员和教师可访问
def update_material(material_id):
    """更新教材"""
    try:
        data = request.get_json()
        material = MaterialService.update_material(material_id, data, request.user_id)
        response = {
            'id': material.id,
            'display_name': material.display_name,
            'category_ids': material.category_ids,
            'type': material.type,
            'updated_at': material.updated_at.isoformat()
        }
        return orjson.dumps(response), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return orjson.dumps({'message': str(e)}), 400, {'Content-Type': 'application/json'}

@material_bp.route('/materials/<int:material_id>', methods=['DELETE'])
@jwt_required(allowed_roles=[1, 2])  # 管理员和教师可访问
def delete_material(material_id):
    """删除教材"""
    try:
        MaterialService.delete_material(material_id)
        return orjson.dumps({'message': '教材删除成功'}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return orjson.dumps({'message': str(e)}), 400, {'Content-Type': 'application/json'}

@material_bp.route('/materials/<int:material_id>/publish', methods=['PUT'])
@jwt_required(allowed_roles=[1, 2])  # 管理员和教师可访问
def toggle_publish(material_id):
    """发布/取消发布教材"""
    try:
        data = request.get_json()
        is_publish = data.get('is_publish')
        if is_publish is None:
            return orjson.dumps({'message': 'is_publish field is required'}), 400, {'Content-Type': 'application/json'}

        material = MaterialService.toggle_publish(material_id, is_publish, request.user_id)
        response = {
            'id': material.id,
            'display_name': material.display_name,
            'publish_status': material.publish_status,
            'updated_at': material.updated_at.isoformat()
        }
        return orjson.dumps(response), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return orjson.dumps({'message': str(e)}), 400, {'Content-Type': 'application/json'}

@material_bp.route('/materials/<int:material_id>/content', methods=['GET'])
@jwt_required()  # 所有角色可访问
def get_material_content(material_id):
    """获取教材内容"""
    try:
        content = MaterialService.get_material_content(material_id)
        return orjson.dumps({'content': content}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return orjson.dumps({'message': str(e)}), 400, {'Content-Type': 'application/json'}

@material_bp.route('/materials/<int:material_id>/content', methods=['PUT'])
@jwt_required(allowed_roles=[1, 2])  # 管理员和教师可访问
def save_material_content(material_id):
    """保存教材内容"""
    try:
        data = request.get_json()
        content = data.get('content')
        if content is None:
            return orjson.dumps({'message': 'content field is required'}), 400, {'Content-Type': 'application/json'}

        material = MaterialService.save_material_content(material_id, content, request.user_id)
        response = {
            'id': material.id,
            'display_name': material.display_name,
            'updated_at': material.updated_at.isoformat()
        }
        return orjson.dumps(response), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return orjson.dumps({'message': str(e)}), 400, {'Content-Type': 'application/json'} 