from peewee import *
from app.models.base import BaseModel
from app.models.user import User
from app.models.material import Material

class Comment(BaseModel):
    material = ForeignKeyField(Material, backref='comments')
    user = ForeignKeyField(User, backref='comments')
    content = TextField()

    class Meta:
        table_name = 'comments' 