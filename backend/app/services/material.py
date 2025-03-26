from typing import List, Optional, Dict
from app.models.material import Material
from app.models.blob import Blob
from app.utils.pagination import paginate_query
from app.exceptions.customer_exceptions import NotFoundException, ValidationException
from peewee import fn
import operator
from functools import reduce
from datetime import datetime
from flask import request, current_app
import os
import hashlib
from werkzeug.utils import secure_filename
import mimetypes
import shutil

class MaterialService:
    @staticmethod
    def _calculate_sha256(file_data: bytes) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_data)
        return sha256_hash.hexdigest()

    @staticmethod
    def _get_file_path(filename: str, sha256: str) -> str:
        sub_dir = sha256[:2]
        upload_folder = current_app.config['UPLOAD_FOLDER']
        directory = os.path.join(upload_folder, sub_dir)
        os.makedirs(directory, exist_ok=True)
        return os.path.join(directory, f"{sha256}_{secure_filename(filename)}")

    @staticmethod
    def get_materials(
        page: int = 1,
        page_size: int = 10,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        category_ids: Optional[str] = None,
        type: Optional[str] = None
    ) -> Dict:
        query = Material.select()
        if display_name:
            query = query.where(Material.display_name.contains(display_name))
        if description:
            query = query.where(Material.description.contains(description))
        if category_ids:
            category_id_list = category_ids.split(',')
            conditions = [
                fn.FIND_IN_SET(cat_id, Material.category_ids) > 0
                for cat_id in category_id_list
            ]
            query = query.where(conditions[0] if len(conditions) == 1 else reduce(operator.or_, conditions))
        if type:
            query = query.where(Material.material_type == type)
        return paginate_query(query, page, page_size)

    @staticmethod
    def create_material(data: Dict, current_user_id: int) -> Material:
        """创建教材"""
        # 验证必填字段
        required_fields = ['display_name', 'category_ids', 'material_type']
        for field in required_fields:
            if field not in data:
                raise ValidationException(f"Missing required field: {field}")

        # 处理文件上传
        blob_id = None
        if 'file' not in request.files:
            raise ValidationException("File is required for upload type material")
        
        file = request.files['file']
        if file.filename == '':
            raise ValidationException("No file selected")

        try:
            # 获取文件信息
            filename = secure_filename(file.filename)
            mime_type = file.content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'

            # 创建临时文件
            temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp', filename)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            file.save(temp_path)

            # 计算文件大小和SHA256
            file_size = os.path.getsize(temp_path)
            with open(temp_path, 'rb') as f:
                sha256 = MaterialService._calculate_sha256(f.read())

            # 检查是否已存在相同的文件
            existing_blob = Blob.get_or_none(Blob.sha256 == sha256)
            if existing_blob:
                blob_id = existing_blob.id
                # 删除临时文件
                os.remove(temp_path)
            else:
                # 生成最终存储路径
                file_path = MaterialService._get_file_path(filename, sha256)
                
                # 移动文件到最终位置
                shutil.move(temp_path, file_path)

                # 创建数据库记录
                blob = Blob.create(
                    file_name=filename,
                    file_path=file_path,
                    mime_type=mime_type,
                    file_size=file_size,
                    sha256=sha256
                )
                blob_id = blob.id

        except Exception as e:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise ValidationException(f"File upload failed: {str(e)}")

        # 添加创建者和更新者信息
        data['created_by'] = current_user_id
        data['updated_by'] = current_user_id
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        
        # 如果是上传类型，添加blob_id
        data['blob_id'] = blob_id

        # 创建教材
        material = Material.create(**data)
        return material

    @staticmethod
    def update_material(material_id: int, data: Dict, current_user_id: int) -> Material:
        material = Material.get_or_none(Material.id == material_id)
        if not material:
            raise NotFoundException("Material not found")
        data['updated_by'] = request.user_id
        data['updated_at'] = datetime.now()
        for key, value in data.items():
            setattr(material, key, value)
        material.save()
        return material

    @staticmethod
    def delete_material(material_id: int) -> None:
        material = Material.get_or_none(Material.id == material_id)
        if not material:
            raise NotFoundException("Material not found")
        material.delete_instance()

    @staticmethod
    def toggle_publish(material_id: int, is_publish: bool, current_user_id: int) -> Material:
        material = Material.get_or_none(Material.id == material_id)
        if not material:
            raise NotFoundException("Material not found")

        material.publish_status = 'public' if is_publish else 'private'
        material.updated_by = request.user_id
        material.updated_at = datetime.now()
        material.save()
        return material

    @staticmethod
    def get_material_content(material_id: int) -> str:
        material = Material.get_or_none(Material.id == material_id)
        if not material:
            raise NotFoundException("Material not found")
        blob = Blob.get_or_none(Blob.id == material.blob_id)
        if not blob:
            raise NotFoundException("Material blob not found")
        with open(blob.file_path, 'rb') as file:
            content = file.read()
        return content.decode('utf-8')
    @staticmethod
    def save_material_content(material_id: int, content: str, current_user_id: int) -> Material:
        material = Material.get_or_none(Material.id == material_id)
        if not material:
            raise NotFoundException("Material not found")

        if material.material_type != 'create':
            raise ValidationException("Cannot save content for upload type material")

        material.updated_by = request.user_id
        material.updated_at = datetime.now()
        material.save()
        return material 