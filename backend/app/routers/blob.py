from flask import Blueprint, request, jsonify, send_file, current_app
from app.utils.jwt import jwt_required
from app.services.blob_service import BlobService
from werkzeug.utils import secure_filename
import os
import mimetypes

blob_bp = Blueprint('blob', __name__)

# 设置最大文件大小为2MB
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB in bytes

@blob_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 检查文件大小
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File size exceeds 2MB limit'}), 400

    try:
        # 获取文件信息
        filename = secure_filename(file.filename)
        mime_type = file.content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        # 创建临时文件
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp', filename)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        file.save(temp_path)

        # 创建blob记录
        blob = BlobService.create_blob(temp_path, filename, mime_type)
        
        return jsonify({
            'id': blob.id,
            'filename': blob.file_name,
            'mime_type': blob.mime_type,
            'file_size': blob.file_size
        }), 201

    except Exception as e:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 400

@blob_bp.route('/preview/<int:blob_id>', methods=['GET'])
def get_file(blob_id):
    """获取文件内容"""
    try:
        blob = BlobService.get_blob(blob_id)
        if not blob:
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            blob.file_path,
            mimetype=blob.mime_type,
            as_attachment=False
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blob_bp.route('/delete/<int:blob_id>', methods=['DELETE'])
@jwt_required()
def delete_file(blob_id):
    """删除文件"""
    try:
        BlobService.delete_blob(blob_id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400 