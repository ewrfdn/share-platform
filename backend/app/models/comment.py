from peewee import *
from .base import BaseModel
from .user import User
from .material import Material

class Comment(BaseModel):
    material = ForeignKeyField(Material, backref='comments')
    user = ForeignKeyField(User, backref='comments')
    content = TextField()

    class Meta:
        table_name = 'comments' 