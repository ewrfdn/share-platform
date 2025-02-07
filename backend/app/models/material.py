from peewee import *
from app.models.base import BaseModel
from app.models.blob import Blob

class Material(BaseModel):
    display_name = CharField()
    category_ids = CharField()  # 存储为逗号分隔的ID字符串
    blob_id = ForeignKeyField(Blob, backref='materials')
    description = TextField(null=True)
    cover = CharField(null=True)  # 封面图片路径

    class Meta:
        table_name = 'materials'

    def get_category_ids(self):
        """将category_ids字符串转换为列表"""
        return [int(id_) for id_ in self.category_ids.split(',') if id_]

    def set_category_ids(self, ids):
        """将分类ID列表转换为字符串存储"""
        self.category_ids = ','.join(str(id_) for id_ in ids) 