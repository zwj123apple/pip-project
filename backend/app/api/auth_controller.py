from flask import Blueprint, request
from pydantic import ValidationError
import logging
import traceback
from app.schemas.user_schema import (
    UserLoginSchema,
    UserResponseSchema
)
from app.services.auth_service import AuthService
from app.utils.jwt_utils import token_required, user_type_required
from app.utils.response import ApiResponse
from app.utils.exceptions import (
    BaseException as CustomBaseException,
    BadRequestException,
    ForbiddenException,
    UnauthorizedException
)

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    try:
        data = request.get_json() or {}
        login_data = UserLoginSchema(**data)

        result = AuthService.login_user(login_data)

        return ApiResponse.success(
            data={
                'access_token': result['access_token'],
                'token_type': result['token_type'],
                'user': UserResponseSchema.model_validate(
                    result['user']
                ).model_dump()
            },
            msg='登录成功'
        )

    except ValidationError as e:
        logger.error(f"登录数据验证失败: {e.errors()}")
        return ApiResponse.validation_error('数据验证失败', e.errors())

    except (BadRequestException, UnauthorizedException, ForbiddenException) as e:
        logger.warning(f"登录认证失败: {e.message}")
        return ApiResponse.auth_error(e.message)

    except CustomBaseException as e:
        logger.error(f"登录业务错误: {e.message}")
        return ApiResponse.error(msg=e.message)

    except Exception as e:
        logger.error(f"登录服务器内部错误: {str(e)}")
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        return ApiResponse.server_error(f'服务器内部错误: {str(e)}')



@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """用户退出登录"""
    try:
        user_id = request.current_user.get('user_id')
        user = AuthService.get_current_user_info(user_id)

        return ApiResponse.success(
            data={'username': user.user_name},
            msg='成功退出登录'
        )

    except CustomBaseException as e:
        logger.error(f"登出业务错误: {e.message}")
        return ApiResponse.error(msg=e.message)
    except Exception as e:
        logger.error(f"登出服务器内部错误: {str(e)}")
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        return ApiResponse.server_error(str(e))


@auth_bp.route('/test', methods=['GET'])
@token_required
def test_token():
    """测试Token有效性的接口"""
    try:
        user_id = request.current_user.get('user_id')
        username = request.current_user.get('username')
        user_type = request.current_user.get('user_type')

        return ApiResponse.success(
            data={
                'user_id': user_id,
                'username': username,
                'user_type': user_type
            },
            msg='Token验证成功'
        )

    except CustomBaseException as e:
        logger.error(f"Token测试业务错误: {e.message}")
        return ApiResponse.error(msg=e.message)
    except Exception as e:
        logger.error(f"Token测试服务器内部错误: {str(e)}")
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        return ApiResponse.server_error(str(e))
