from app.crud.user_crud import UserCrud
from app.utils.jwt_utils import create_access_token
from app.utils.exceptions import (
    UnauthorizedException,
    
)


class AuthService:
    """认证服务层"""

    @staticmethod
    def login_user(login_data):
        """用户登录"""
        user = UserCrud.authenticate_user(
            login_data.user_name,
            login_data.password,
        )

        if not user:
            raise UnauthorizedException('用户名或密码错误')

        # 生成 JWT token
        access_token = create_access_token(
            user_id=user.id,
            username=user.user_name,
            user_type=user.user_type
        )

        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'user': user
        }

    @staticmethod
    def get_current_user_info(user_id):
        """获取当前用户信息"""
        user = UserCrud.get_user_by_id(user_id)
        if not user:
            raise UnauthorizedException('User not found')
        return user
