from peewee import *
from app.models.base import BaseModel

class Blob(BaseModel):
    file_name = CharField()
    file_path = CharField()
    mime_type = CharField()
    file_size = BigIntegerField()  # 使用BigIntegerField存储文件大小
    sha256 = CharField()

    class Meta:
        table_name = 'blobs' 