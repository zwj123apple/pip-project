"""
Service层测试
"""
import pytest
from app.services.auth_service import AuthService
from app.services.loan_service import LoanService
from app.utils.exceptions import UnauthorizedException
from app.models.user import User


class TestAuthService:
    """测试认证服务"""
    
    def test_login_user_success(self, db, enterprise_user):
        """测试登录成功"""
        from app.schemas.user_schema import UserLoginSchema
        
        login_data = UserLoginSchema(
            user_name=enterprise_user.user_name,
            password='Test1234'
        )
        
        result = AuthService.login_user(login_data)
        
        assert 'access_token' in result
        assert result['user'].id == enterprise_user.id
    
    def test_login_user_wrong_password(self, db, enterprise_user):
        """测试错误密码"""
        from app.schemas.user_schema import UserLoginSchema
        
        login_data = UserLoginSchema(
            user_name=enterprise_user.user_name,
            password='WrongPassword'
        )
        
        with pytest.raises(UnauthorizedException):
            AuthService.login_user(login_data)
    
    def test_login_user_not_found(self, db):
        """测试用户不存在"""
        from app.schemas.user_schema import UserLoginSchema
        
        login_data = UserLoginSchema(
            user_name='nonexistent',
            password='Pass1234'
        )
        
        with pytest.raises(UnauthorizedException):
            AuthService.login_user(login_data)
    
    def test_get_current_user_info(self, db, enterprise_user):
        """测试获取当前用户信息"""
        user = AuthService.get_current_user_info(enterprise_user.id)
        assert user.id == enterprise_user.id
    
    def test_get_current_user_info_not_found(self, db):
        """测试获取不存在的用户"""
        with pytest.raises(UnauthorizedException):
            AuthService.get_current_user_info(99999)


class TestLoanService:
    """测试贷款服务"""
    
    def test_upload_file_only(self, app, mock_file):
        """测试文件上传"""
        with app.app_context():
            result = LoanService.upload_file_only(mock_file)
            
            assert result is not None
            assert 'file_path' in result
            assert 'file_name' in result
    
    def test_upload_file_none(self, app):
        """测试上传空文件"""
        with app.app_context():
            result = LoanService.upload_file_only(None)
            
            assert result['file_path'] is None
            assert result['file_name'] is None
    
    def test_save_to_database(self, db, sample_loan_data):
        """测试保存到数据库"""
        data = sample_loan_data.copy()
        data['prop_proof_docs'] = '/uploads/test.pdf'
        data['prop_proof_docs_name'] = 'test.pdf'
        
        loan = LoanService.save_to_database(data)
        
        assert loan is not None
        assert loan.ent_name == data['ent_name']
    
    def test_get_chart_data(self, app):
        """测试获取图表数据"""
        with app.app_context():
            data = LoanService.get_chart_data()
            assert isinstance(data, list)