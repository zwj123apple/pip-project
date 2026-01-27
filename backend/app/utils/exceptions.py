class BaseException(Exception):
    """基础异常类"""
    def __init__(self, message, code=500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class UnauthorizedException(BaseException):
    """未授权异常"""
    def __init__(self, message='Unauthorized'):
        super().__init__(message, 401)


class ForbiddenException(BaseException):
    """禁止访问异常"""
    def __init__(self, message='Forbidden'):
        super().__init__(message, 403)


class NotFoundException(BaseException):
    """未找到异常"""
    def __init__(self, message='Not found'):
        super().__init__(message, 404)


class BadRequestException(BaseException):
    """错误请求异常"""
    def __init__(self, message='Bad request'):
        super().__init__(message, 400)


class ConflictException(BaseException):
    """冲突异常"""
    def __init__(self, message='Conflict'):
        super().__init__(message, 409)