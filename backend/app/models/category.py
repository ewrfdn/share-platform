from peewee import *
from app.models.base import BaseModel

class Category(BaseModel):
    display_name = CharField()
    parent_id = IntegerField(null=True)  # 允许为空,表示顶级分类

    class Meta:
        table_name = 'categories' 