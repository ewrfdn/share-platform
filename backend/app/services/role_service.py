from typing import List
from app.models.role import Role

class RoleService:
    @staticmethod
    def get_all_roles() -> List[Role]:
        """获取所有角色"""
        return Role.select()
