from datetime import datetime
from peewee import Model
from app.database import db
from peewee import *
import pytz

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    id = PrimaryKeyField()
    class Meta:
        database = db
        charset = 'utf8mb4'

    def to_json(self):
        item = {}
        for column, column_info in self._meta.fields.items():
            try:
                column_type = type(column_info)
                column_value = getattr(self, column)
                item[column] = self._normalize_model_field(column_value, column_type)
            except Exception as e:
                print(e)
                pass
        return item

    @staticmethod
    def _normalize_model_field(value, field_type):
        if value is None:
            return None

        if isinstance(value, str):
            return value

        # Handle model instances (for joined queries)
        if isinstance(value, Model):
            return value.to_json() if hasattr(value, 'to_json') else str(value)

        if field_type == UUIDField:
            return str(value)
        elif field_type == DateTimeField:
            return value.astimezone(pytz.timezone("Asia/Shanghai")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        elif field_type == DateField:
            return value.strftime("%Y-%m-%d")
        elif isinstance(field_type, (ForeignKeyField, DeferredForeignKey)):
            # Handle foreign key fields
            if isinstance(value, Model):
                return value.to_json() if hasattr(value, 'to_json') else str(value)
            return value
        return value

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)