"""
统一API响应格式工具类
"""
from flask import jsonify
from datetime import datetime


class ApiResponse:
    """统一API响应类"""
    
    # 成功状态码
    SUCCESS_CODE = 0
    
    # 错误状态码
    ERROR_CODE = 10001
    VALIDATION_ERROR = 10002
    AUTH_ERROR = 10003
    NOT_FOUND_ERROR = 10004
    FILE_ERROR = 10005
    SERVER_ERROR = 10006
    
    @staticmethod
    def success(data=None, msg="成功"):
        """
        成功响应
        :param data: 响应数据
        :param msg: 响应消息
        :return: Flask响应对象
        """
        response = jsonify({
            "code": ApiResponse.SUCCESS_CODE,
            "msg": msg,
            "data": data or {},
            "timestamp": int(datetime.now().timestamp())
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 200
    
    @staticmethod
    def error(code=ERROR_CODE, msg="失败", data=None):
        """
        错误响应
        :param code: 错误码
        :param msg: 错误消息
        :param  附加数据
        :return: Flask响应对象
        """
        response = jsonify({
            "code": code,
            "msg": msg,
            "data": data or {},
            "timestamp": int(datetime.now().timestamp())
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 200
    
    @staticmethod
    def validation_error(msg="数据验证失败", errors=None):
        """验证错误响应"""
        return ApiResponse.error(
            code=ApiResponse.VALIDATION_ERROR,
            msg=msg,
            data={"errors": errors} if errors else {}
        )
    
    @staticmethod
    def auth_error(msg="认证失败"):
        """认证错误响应"""
        return ApiResponse.error(
            code=ApiResponse.AUTH_ERROR,
            msg=msg
        )
    
    @staticmethod
    def not_found_error(msg="资源不存在"):
        """资源不存在响应"""
        return ApiResponse.error(
            code=ApiResponse.NOT_FOUND_ERROR,
            msg=msg
        )
    
    @staticmethod
    def file_error(msg="文件处理失败"):
        """文件错误响应"""
        return ApiResponse.error(
            code=ApiResponse.FILE_ERROR,
            msg=msg
        )
    
    @staticmethod
    def server_error(msg="服务器错误"):
        """服务器错误响应"""
        return ApiResponse.error(
            code=ApiResponse.SERVER_ERROR,
            msg=msg
        )
