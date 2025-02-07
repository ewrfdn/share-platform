from flask import Blueprint, request, jsonify
from app.services.blob_service import BlobService
from app.utils.jwt import jwt_required

blob_bp = Blueprint('blob', __name__)

@jwt_required
@blob_bp.route('/upload', methods=['POST'])
def upload_file():
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'message': '没有文件被上传'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': '没有选择文件'}), 400

    try:
        blob, is_new = BlobService.create_blob(file)
        return jsonify({
            'id': blob.id,
            'file_name': blob.file_name,
            'file_size': blob.file_size,
            'mime_type': blob.mime_type,
            'is_new': is_new
        }), 201
    except Exception as e:
        return jsonify({'message': f'上传失败: {str(e)}'}), 500

@jwt_required
@blob_bp.route('/preview/<int:blob_id>', methods=['GET'])
def get_file(blob_id):
    """获取文件"""
    try:
        return BlobService.get_file_content(blob_id)
    except FileNotFoundError as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'获取文件失败: {str(e)}'}), 500

@jwt_required
@blob_bp.route('/delete/<int:blob_id>', methods=['DELETE'])
def delete_file(blob_id):
    """删除文件"""
    if BlobService.delete_blob(blob_id):
        return jsonify({'message': '文件删除成功'}), 200
    return jsonify({'message': '文件不存在'}), 404 