from peewee import *
from app.models.base import BaseModel
from app.models.user import User

class Category(BaseModel):
    display_name = CharField()
    parent_id = IntegerField(null=True)  # 允许为空,表示顶级分类
    created_by = ForeignKeyField(User, null=True, on_delete='SET NULL', column_name='created_by')
    updated_by = ForeignKeyField(User, null=True, on_delete='SET NULL', column_name='updated_by')
    class Meta:
        table_name = 'categories' 