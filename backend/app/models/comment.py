from peewee import *
from app.models.base import BaseModel
from app.models.user import User
from app.models.material import Material


class Comment(BaseModel):
    material = ForeignKeyField(Material, backref='comments')
    user = ForeignKeyField(User, backref='comments')
    content = TextField()
    created_by = ForeignKeyField(User, null=True, on_delete='SET NULL', column_name='created_by')
    updated_by = ForeignKeyField(User, null=True, on_delete='SET NULL', column_name='updated_by')

    class Meta:
        table_name = 'comments' 