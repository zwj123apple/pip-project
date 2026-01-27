import jwt
from datetime import datetime, timezone
from functools import wraps
from flask import request, current_app
from app.utils.exceptions import UnauthorizedException


def create_access_token(user_id, username, user_type):
    """创建 JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'user_type': user_type,
        'exp': datetime.now(timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.now(timezone.utc)
}
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )
    return token


def decode_token(token):
    """解码 JWT token"""
    try:
        # 添加验证选项，确保验证过期时间
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=[current_app.config['JWT_ALGORITHM']],
            options={
                'verify_signature': True,
                'verify_exp': True,  # 验证过期时间
                'verify_iat': True,  # 验证签发时间
                'require_exp': True,  # 要求必须有exp字段
                'require_iat': True   # 要求必须有iat字段
            }
        )
        
        # 额外的调试日志
        import logging
        logging.info(f"Token验证成功 - exp: {payload.get('exp')}, 当前时间: {datetime.now(timezone.utc).timestamp()}")
        
        return payload
    except jwt.ExpiredSignatureError as e:
        import logging
        logging.warning(f"Token已过期: {str(e)}")
        raise UnauthorizedException('Token已过期，请重新登录')
    except jwt.InvalidTokenError as e:
        import logging
        logging.warning(f"无效的Token: {str(e)}")
        raise UnauthorizedException('无效的Token')


def token_required(f):
    """JWT 认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # 延迟导入避免循环依赖
        from app.utils.response import ApiResponse
        
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return ApiResponse.auth_error('Token格式错误')

        if not token:
            return ApiResponse.auth_error('缺少Token')

        try:
            payload = decode_token(token)
            request.current_user = payload
        except UnauthorizedException as e:
            return ApiResponse.auth_error(str(e))

        return f(*args, **kwargs)

    return decorated