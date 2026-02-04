"""
贷款API测试 - 100%覆盖率
"""
import pytest
import json
from io import BytesIO
from werkzeug.datastructures import FileStorage


class TestLoanApply:
    """测试贷款申请接口 /api/loan/apply"""
    
    def test_apply_success_with_file(self, client, db, auth_headers_enterprise, sample_loan_data, mock_file):
        """测试成功提交贷款申请（带文件）"""
        data = sample_loan_data.copy()
        data['prop_proof_docs'] = mock_file
        
        response = client.post(
            '/api/loan/apply',
            data=data,
            headers=auth_headers_enterprise,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] == 0
        assert 'file_info' in json_data['data']
        assert 'financial_data' in json_data['data']
    
    def test_apply_without_token(self, client, db, sample_loan_data, mock_file):
        """测试未登录提交申请"""
        data = sample_loan_data.copy()
        data['prop_proof_docs'] = mock_file
        
        response = client.post(
            '/api/loan/apply',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
    
    def test_apply_without_file(self, client, db, auth_headers_enterprise, sample_loan_data):
        """测试未上传文件"""
        response = client.post(
            '/api/loan/apply',
            data=sample_loan_data,
            headers=auth_headers_enterprise,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
        assert '文件' in json_data['msg'] or 'file' in json_data['msg'].lower()
    
    def test_apply_missing_required_fields(self, client, db, auth_headers_enterprise, mock_file):
        """测试缺少必填字段"""
        incomplete_data = {
            'ent_name': '测试企业',
            'prop_proof_docs': mock_file
        }
        
        response = client.post(
            '/api/loan/apply',
            data=incomplete_data,
            headers=auth_headers_enterprise,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
    
    def test_apply_invalid_uscc(self, client, db, auth_headers_enterprise, sample_loan_data, mock_file):
        """测试无效的统一社会信用代码"""
        data = sample_loan_data.copy()
        data['uscc'] = '123'
        data['prop_proof_docs'] = mock_file
        
        response = client.post(
            '/api/loan/apply',
            data=data,
            headers=auth_headers_enterprise,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
    
    def test_apply_invalid_loan_term_for_credit(self, client, db, auth_headers_enterprise, sample_loan_data, mock_file):
        """测试信用贷款超期限"""
        data = sample_loan_data.copy()
        data['loan_purpose'] = 'credit'
        data['loan_term'] = '6'
        data['prop_proof_docs'] = mock_file
        
        response = client.post(
            '/api/loan/apply',
            data=data,
            headers=auth_headers_enterprise,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0


class TestLoanConfirm:
    """测试贷款确认接口 /api/loan/confirm"""
    
    def test_confirm_success(self, client, db, auth_headers_enterprise, sample_loan_data):
        """测试成功确认贷款申请"""
        data = sample_loan_data.copy()
        data['prop_proof_docs'] = '/uploads/test.pdf'
        data['prop_proof_docs_name'] = 'test.pdf'
        
        response = client.post(
            '/api/loan/confirm',
            data=data,
            headers=auth_headers_enterprise,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] == 0
    
    def test_confirm_without_token(self, client, db, sample_loan_data):
        """测试未登录确认申请"""
        data = sample_loan_data.copy()
        data['prop_proof_docs'] = '/uploads/test.pdf'
        
        response = client.post(
            '/api/loan/confirm',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0
    
    def test_confirm_missing_fields(self, client, db, auth_headers_enterprise):
        """测试确认时缺少字段"""
        incomplete_data = {'ent_name': '测试企业'}
        
        response = client.post(
            '/api/loan/confirm',
            data=incomplete_data,
            headers=auth_headers_enterprise,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] != 0