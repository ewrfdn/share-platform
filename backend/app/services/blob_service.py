import os
import hashlib
from werkzeug.utils import secure_filename
from flask import current_app, send_file
from ..models.blob import Blob
from typing import Optional, Tuple
import mimetypes

class BlobService:
    @staticmethod
    def _calculate_sha256(file_data: bytes) -> str:
        """计算文件的SHA256哈希值"""
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_data)
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

    @classmethod
    def create_blob(cls, file) -> Tuple[Blob, bool]:
        """
        创建文件记录
        返回: (blob对象, 是否为新创建)
        """
        try:
            # 读取文件内容
            file_data = file.read()
            file.seek(0)  # 重置文件指针位置
            
            # 获取文件信息
            filename = secure_filename(file.filename)
            file_size = len(file_data)
            sha256 = cls._calculate_sha256(file_data)
            mime_type = file.content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'

            # 检查是否已存在相同的文件
            existing_blob = Blob.get_or_none(Blob.sha256 == sha256)
            if existing_blob:
                return existing_blob, False

            # 生成存储路径
            file_path = cls._get_file_path(filename, sha256)

            # 保存文件
            file.save(file_path)

            # 创建数据库记录
            blob = Blob.create(
                file_name=filename,
                file_path=file_path,
                mime_type=mime_type,
                file_size=file_size,
                sha256=sha256
            )

            return blob, True

        except Exception as e:
            current_app.logger.error(f"创建Blob失败: {str(e)}")
            raise

    @staticmethod
    def get_blob_by_id(blob_id: int) -> Optional[Blob]:
        """根据ID获取Blob记录"""
        return Blob.get_or_none(Blob.id == blob_id)

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

    @staticmethod
    def delete_blob(blob_id: int) -> bool:
        """删除Blob记录及对应的文件"""
        blob = Blob.get_or_none(Blob.id == blob_id)
        if not blob:
            return False

        # 删除物理文件
        if os.path.exists(blob.file_path):
            os.remove(blob.file_path)

        # 删除数据库记录
        blob.delete_instance()
        return True 