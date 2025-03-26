import os
import hashlib
import shutil
from werkzeug.utils import secure_filename
from flask import current_app, send_file
from app.models.blob import Blob
from typing import Optional, Tuple
import mimetypes
from app.exceptions.customer_exceptions import NotFoundException, ValidationException

class BlobService:
    @staticmethod
    def _calculate_sha256(file_path: str) -> str:
        """计算文件的SHA256哈希值"""
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    @staticmethod
    def _get_file_path(filename: str, sha256: str) -> str:
        """生成文件存储路径"""
        # 使用sha256的前两位作为子目录，防止单个目录文件过多
        sub_dir = sha256[:2]
        upload_folder = current_app.config['UPLOAD_FOLDER']
        directory = os.path.join(upload_folder, sub_dir)
        
        # 确保目录存在
        os.makedirs(directory, exist_ok=True)
        
        # 返回完整的文件路径
        return os.path.join(directory, f"{sha256}_{secure_filename(filename)}")

    @staticmethod
    def create_blob(temp_path: str, filename: str, mime_type: str) -> Blob:
        """创建blob记录"""
        try:
            # 计算文件大小和SHA256
            file_size = os.path.getsize(temp_path)
            sha256 = BlobService._calculate_sha256(temp_path)

            # 检查是否已存在相同的文件
            existing_blob = Blob.get_or_none(Blob.sha256 == sha256)
            if existing_blob:
                # 删除临时文件
                os.remove(temp_path)
                return existing_blob

            # 生成最终存储路径
            file_path = BlobService._get_file_path(filename, sha256)
            
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
            return blob

        except Exception as e:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise ValidationException(f"Failed to create blob: {str(e)}")

    @staticmethod
    def get_blob(blob_id: int) -> Blob:
        """获取blob记录"""
        blob = Blob.get_or_none(Blob.id == blob_id)
        if not blob:
            raise NotFoundException(f"Blob with id {blob_id} not found")
        return blob

    @staticmethod
    def delete_blob(blob_id: int) -> None:
        """删除blob记录和文件"""
        blob = BlobService.get_blob(blob_id)
        
        # 删除文件
        if os.path.exists(blob.file_path):
            os.remove(blob.file_path)
        
        # 删除数据库记录
        blob.delete_instance()

    @staticmethod
    def get_file_content(blob_id: int):
        """获取文件内容"""
        blob = Blob.get_or_none(Blob.id == blob_id)
        if not blob:
            raise FileNotFoundError(f"找不到ID为{blob_id}的文件")

        if not os.path.exists(blob.file_path):
            raise FileNotFoundError(f"文件{blob.file_path}不存在")

        return send_file(
            blob.file_path,
            mimetype=blob.mime_type,
            as_attachment=True,
            download_name=blob.file_name
        ) 