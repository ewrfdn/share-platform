from peewee import *
from .base import BaseModel

class Role(BaseModel):
    display_name = CharField()

    class Meta:
        table_name = 'roles' 