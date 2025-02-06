from typing import List, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..models.role import Role
from flask import abort

class UserService:
    @staticmethod
    def get_all_users() -> List[User]:
        """获取所有用户"""
        return User.select()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return User.get_or_none(User.id == user_id)

    @staticmethod
    def create_user(username: str, password: str, role_id: int, current_user_role_id: int) -> User:
        """
        创建用户
        :param username: 用户名
        :param password: 密码
        :param role_id: 角色ID
        :param current_user_role_id: 当前操作用户的角色ID
        """
        # 检查权限
        if current_user_role_id == 2:  # 老师
            if role_id != 3:  # 老师只能创建学生
                abort(403, description="老师只能创建学生账号")
        elif current_user_role_id == 1:  # 管理员可以创建所有类型用户
            pass
        else:
            abort(403, description="没有创建用户的权限")

        # 检查用户名是否已存在
        if User.get_or_none(User.username == username):
            abort(400, description="用户名已存在")

        # 创建用户
        return User.create(
            username=username,
            password=generate_password_hash(password),
            role_id=role_id
        )

    @staticmethod
    def delete_user(user_id: int, current_user_role_id: int) -> bool:
        """
        删除用户
        :param user_id: 要删除的用户ID
        :param current_user_role_id: 当前操作用户的角色ID
        """
        user = User.get_or_none(User.id == user_id)
        if not user:
            return False

        # 检查权限
        if current_user_role_id == 2:  # 老师
            if user.role_id != 3:  # 老师只能删除学生
                abort(403, description="老师只能删除学生账号")
        elif current_user_role_id == 1:  # 管理员可以删除所有用户
            pass
        else:
            abort(403, description="没有删除用户的权限")

        user.delete_instance()
        return True

class RoleService:
    @staticmethod
    def get_all_roles() -> List[Role]:
        """获取所有角色"""
        return Role.select() 