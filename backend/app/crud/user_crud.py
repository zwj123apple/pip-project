from app.models.user import User

class UserCrud:
    """用户数据访问层"""

    @staticmethod
    def get_user_by_username(user_name):
        """通过用户名获取用户"""
        return User.query.filter_by(user_name=user_name).first()

    @staticmethod
    def get_user_by_id(user_id):
        """通过 ID 获取用户"""
        return User.query.get(user_id)

    @staticmethod
    def authenticate_user(user_name, password):
        """验证用户登录"""
        user = UserCrud.get_user_by_username(user_name)
        if user and user.check_password(password):
            return user
        return None