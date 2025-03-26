from peewee import *
from app.models.base import BaseModel
from app.models.user import User

class Role(BaseModel):
    display_name = CharField()
    created_by = ForeignKeyField(User, null=True, on_delete='SET NULL', column_name='created_by')
    updated_by = ForeignKeyField(User, null=True, on_delete='SET NULL', column_name='updated_by')
    class Meta:
        table_name = 'roles' 