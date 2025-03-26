from peewee import *
from app.models.base import BaseModel
from app.models.user import User

class Blob(BaseModel):
    file_name = CharField()
    file_path = CharField()
    mime_type = CharField()
    file_size = BigIntegerField()  # 使用BigIntegerField存储文件大小
    sha256 = CharField()
    created_by = ForeignKeyField(User, null=True, on_delete='SET NULL', column_name='created_by')
    updated_by = ForeignKeyField(User, null=True, on_delete='SET NULL', column_name='updated_by')
    class Meta:
        table_name = 'blobs' 