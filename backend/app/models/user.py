from peewee import *
from datetime import datetime
from app.models.base import BaseModel

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    role_id = IntegerField()
    avatar = CharField(null=True)
    
    class Meta:
        table_name = 'users' 