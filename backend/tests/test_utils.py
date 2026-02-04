"""
工具函数测试
"""
import pytest
import jwt
from datetime import datetime, timedelta
from app.utils.jwt_utils import create_access_token, decode_token, generate_token
from app.utils.response import ApiResponse
from app.utils.exceptions import (
    UnauthorizedException,
    BadRequestException,
    ForbiddenException
)


class TestJWTUtils:
    """测试JWT工具函数"""
    
    def test_create_access_token(self, app):
        """测试创建访问令牌"""
        with app.app_context():
            token = create_access_token(
                user_id=1,
                username='testuser',
                user_type='ENTERPRISE'
            )
            
            assert token is not None
            assert isinstance(token, str)
    
    def test_decode_token_valid(self, app):
        """测试解码有效令牌"""
        with app.app_context():
            token = create_access_token(
                user_id=1,
                username='testuser',
                user_type='ENTERPRISE'
            )
            
            payload = decode_token(token)
            
            assert payload is not None
            assert payload['user_id'] == 1
            assert payload['username'] == 'testuser'
    
    def test_decode_token_invalid(self, app):
        """测试解码无效令牌"""
        with app.app_context():
            with pytest.raises(Exception):
                decode_token('invalid_token')
    
    def test_generate_token(self, app):
        """测试生成令牌"""
        with app.app_context():
            token = generate_token(1, 'ENTERPRISE')
            assert token is not None


class TestApiResponse:
    """测试API响应工具"""
    
    def test_success_response(self):
        """测试成功响应"""
        response = ApiResponse.success(data={'key': 'value'}, msg='成功')
        json_data = response.get_json()
        
        assert json_data['code'] == 0
        assert json_data['msg'] == '成功'
        assert json_data['data']['key'] == 'value'
    
    def test_error_response(self):
        """测试错误响应"""
        response = ApiResponse.error(msg='错误信息')
        json_data = response.get_json()
        
        assert json_data['code'] != 0
        assert json_data['msg'] == '错误信息'
    
    def test_validation_error(self):
        """测试验证错误响应"""
        errors = [{'field': 'name', 'msg': '不能为空'}]
        response = ApiResponse.validation_error('验证失败', errors)
        json_data = response.get_json()
        
        assert json_data['code'] != 0
        assert 'errors' in json_data['data']
    
    def test_auth_error(self):
        """测试认证错误响应"""
        response = ApiResponse.auth_error('未授权')
        json_data = response.get_json()
        
        assert json_data['code'] != 0
        assert '未授权' in json_data['msg']
    
    def test_server_error(self):
        """测试服务器错误响应"""
        response = ApiResponse.server_error('服务器错误')
        json_data = response.get_json()
        
        assert json_data['code'] != 0
        assert '服务器错误' in json_data['msg']


class TestExceptions:
    """测试自定义异常"""
    
    def test_unauthorized_exception(self):
        """测试未授权异常"""
        with pytest.raises(UnauthorizedException) as exc_info:
            raise UnauthorizedException('未授权访问')
        
        assert '未授权' in str(exc_info.value)
    
    def test_bad_request_exception(self):
        """测试错误请求异常"""
        with pytest.raises(BadRequestException) as exc_info:
            raise BadRequestException('请求参数错误')
        
        assert '错误' in str(exc_info.value)
    
    def test_forbidden_exception(self):
        """测试禁止访问异常"""
        with pytest.raises(ForbiddenException) as exc_info:
            raise ForbiddenException('禁止访问')
        
        assert '禁止' in str(exc_info.value)