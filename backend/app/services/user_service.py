from typing import List, Optional
import bcrypt
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.role import Role
from flask import abort, request

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

        # 密码加密
        password_hash = generate_password_hash(password)

        # 创建用户
        return User.create(
            username=username,
            password=password_hash,
            role_id=role_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=request.user_id,
            updated_by=request.user_id
        )

    @staticmethod
    def delete_user(user_id: int, current_user_role_id: int, current_user_id: int) -> bool:
        """
        删除用户
        :param user_id: 要删除的用户ID
        :param current_user_role_id: 当前操作用户的角色ID
        :param current_user_id: 当前操作用户的ID
        """
        if user_id == 1:
            abort(403, description="不能删除管理员账号")
        user = User.get_or_none(User.id == user_id)
        if not user:
            return False

        # 防止删除自己的账号
        if user_id == current_user_id:
            abort(403, description="不能删除自己的账号")

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

    @staticmethod
    def update_user(user_id: int, username: str, role_id: int, current_user_role_id: int, password: Optional[str] = None, avatar: Optional[str] = None) -> User:
        """
        更新用户
        :param user_id: 用户ID
        :param username: 用户名
        :param role_id: 角色ID
        :param current_user_role_id: 当前操作用户的角色ID
        :param password: 密码
        :param avatar: 头像
        """
        user = User.get_or_none(User.id == user_id)
        if not user:
            raise Exception("用户不存在")

        # 检查权限
        if current_user_role_id == 2:  # 老师
            if user.role_id == 1 or role_id == 1:  # 老师不能修改管理员账户或将其他账户提升为管理员
                abort(403, description="没有权限修改管理员账户或提升为管理员")
        elif current_user_role_id == 1:  # 管理员可以修改所有用户
            pass
        else:
            abort(403, description="没有修改用户的权限")

        # 只更新提供的字段
        if role_id is not None:
            user.role_id = role_id

        if avatar is not None:
            user.avatar = avatar

        if password:
            password_hash = generate_password_hash(password)
            user.password = password_hash

        user.updated_at = datetime.now()
        user.updated_by = request.user_id
        user.save()
        return user

class RoleService:
    @staticmethod
    def get_all_roles() -> List[Role]:
        """获取所有角色"""
        return Role.select()