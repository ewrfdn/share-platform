from flask import Blueprint, request, jsonify
from app.services.category_service import CategoryService
from app.utils.jwt import jwt_required
from app.exceptions.customer_exceptions import NotFoundException, BadRequestException

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories"""
    try:
        categories = CategoryService.get_all_categories()
        return jsonify({
            "data": categories,
            "message": "Categories retrieved successfully"
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@category_bp.route('/categories/tree', methods=['GET'])
@jwt_required()
def get_category_tree():
    """Get categories in tree structure"""
    try:
        tree = CategoryService.get_category_tree()
        return jsonify({
            "data": tree,
            "message": "Category tree retrieved successfully"
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@category_bp.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category_by_id(category_id):
    """Get a specific category by ID"""
    try:
        category = CategoryService.get_category_by_id(category_id)
        return jsonify({
            "data": category,
            "message": "Category retrieved successfully"
        }), 200
    except NotFoundException as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@category_bp.route('/categories/<int:category_id>/children', methods=['GET'])
@jwt_required()
def get_category_children(category_id):
    """Get direct children of a category"""
    try:
        children = CategoryService.get_children(category_id)
        return jsonify({
            "data": children,
            "message": "Category children retrieved successfully"
        }), 200
    except NotFoundException as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@category_bp.route('/categories/<int:category_id>/descendants', methods=['GET'])
@jwt_required()
def get_category_descendants(category_id):
    """Get all descendants of a category"""
    try:
        descendants = CategoryService.get_descendants(category_id)
        return jsonify({
            "data": descendants,
            "message": "Category descendants retrieved successfully"
        }), 200
    except NotFoundException as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@category_bp.route('/categories', methods=['POST'])
@jwt_required(allowed_roles=[1, 2])  # Only admins and teachers can create categories
def create_category():
    """Create a new category"""
    try:
        data = request.get_json()
        
        if 'display_name' not in data:
            return jsonify({"message": "Display name is required"}), 400
            
        category = CategoryService.create_category(
            display_name=data['display_name'],
            parent_id=data.get('parent_id')
        )
        
        return jsonify({
            "data": category,
            "message": "Category created successfully"
        }), 201
    except NotFoundException as e:
        return jsonify({"message": str(e)}), 404
    except BadRequestException as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required(allowed_roles=[1, 2])  # Only admins and teachers can update categories
def update_category(category_id):
    """Update a category"""
    try:
        data = request.get_json()
        update_data = {}
        
        if 'display_name' in data:
            update_data['display_name'] = data['display_name']
            
        if 'parent_id' in data:
            update_data['parent_id'] = data['parent_id']
            
        category = CategoryService.update_category(
            category_id=category_id,
            data=update_data
        )
        
        return jsonify({
            "data": category,
            "message": "Category updated successfully"
        }), 200
    except NotFoundException as e:
        return jsonify({"message": str(e)}), 404
    except BadRequestException as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required(allowed_roles=[1, 2])  # Only admins and teachers can delete categories
def delete_category(category_id):
    """Delete a category"""
    try:
        recursive = request.args.get('recursive', 'false').lower() == 'true'
        
        result = CategoryService.delete_category(category_id, recursive)
        return jsonify(result), 200
    except NotFoundException as e:
        return jsonify({"message": str(e)}), 404
    except BadRequestException as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
