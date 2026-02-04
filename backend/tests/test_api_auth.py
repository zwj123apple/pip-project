"""
认证API测试 - 100%覆盖率
"""
import pytest
import json
from app.models.user import User


class TestAuthLogin:
    """测试用户登录接口"""
    
    def test_login_success(self, client, db, enterprise_user):
        """测试登录成功"""
        data = {
            'user_name': enterprise_user.user_name,
            'password': 'Test1234'
        }
        
        response = client.post(
            '/api/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] == 0
        assert 'access_token' in json_data['data']
        assert json_data['data']['user']['user_name'] == enterprise_user.user_name
    
    def test_login_wrong_password(self, client, db, enterprise_user):
        """测试错误密码"""
        data = {
            'user_name': enterprise_user.user_name,
            'password': 'WrongPassword'
        }
        
        response = client.post(
            '/api/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
        assert '密码' in json_data['msg'] or 'password' in json_data['msg'].lower()
    
    def test_login_nonexistent_user(self, client, db):
        """测试不存在的用户"""
        data = {
            'user_name': 'nonexistent_user',
            'password': 'Pass1234'
        }
        
        response = client.post(
            '/api/auth/login',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
    
    def test_login_missing_fields(self, client, db):
        """测试缺少必填字段"""
        test_cases = [
            {},
            {'user_name': 'test'},
            {'password': 'Pass1234'},
        ]
        
        for data in test_cases:
            response = client.post(
                '/api/auth/login',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data['code'] != 0


class TestAuthLogout:
    """测试用户退出接口"""
    
    def test_logout_success(self, client, db, auth_headers_enterprise):
        """测试退出登录成功"""
        response = client.post(
            '/api/auth/logout',
            headers=auth_headers_enterprise
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] == 0
        assert '成功' in json_data['msg'] or 'success' in json_data['msg'].lower()
    
    def test_logout_without_token(self, client, db):
        """测试未携带token退出"""
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
    
    def test_logout_invalid_token(self, client, db):
        """测试无效token退出"""
        response = client.post(
            '/api/auth/logout',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0


class TestAuthTestToken:
    """测试Token验证接口"""
    
    def test_token_valid(self, client, db, auth_headers_enterprise, enterprise_user):
        """测试有效token"""
        response = client.get(
            '/api/auth/test',
            headers=auth_headers_enterprise
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] == 0
        assert json_data['data']['user_id'] == enterprise_user.id
    
    def test_token_missing(self, client, db):
        """测试缺少token"""
        response = client.get('/api/auth/test')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
    
    def test_token_invalid(self, client, db):
        """测试无效token"""
        response = client.get(
            '/api/auth/test',
            headers={'Authorization': 'Bearer invalid_token_string'}
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
    
    def test_token_malformed(self, client, db):
        """测试格式错误的Authorization头"""
        test_cases = [
            {'Authorization': 'invalid'},
            {'Authorization': 'Bear token'},
            {'Authorization': ''},
        ]
        
        for headers in test_cases:
            response = client.get('/api/auth/test', headers=headers)
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data['code'] != 0