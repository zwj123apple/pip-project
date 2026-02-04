"""
Pytest配置和fixture定义
"""
import os
import sys
import pytest
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db as _db
from app.models.user import User
from app.models.loan_application import LoanApplication
from app.utils.jwt_utils import generate_token


@pytest.fixture(scope='session')
def app():
    """创建测试用的Flask应用"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'JWT_SECRET_KEY': 'test-jwt-secret',
    })
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """为每个测试函数创建新的数据库会话"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app, db):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """创建CLI测试runner"""
    return app.test_cli_runner()


@pytest.fixture
def enterprise_user(db):
    """创建企业用户"""
    user = User(
        user_name='enterprise_test',
        password='Test1234',
        user_type='ENTERPRISE'
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def individual_user(db):
    """创建个人用户"""
    user = User(
        user_name='individual_test',
        password='Test1234',
        user_type='INDIVIDUAL'
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def enterprise_token(enterprise_user):
    """生成企业用户token"""
    return generate_token(enterprise_user.id, enterprise_user.user_type)


@pytest.fixture
def individual_token(individual_user):
    """生成个人用户token"""
    return generate_token(individual_user.id, individual_user.user_type)


@pytest.fixture
def auth_headers_enterprise(enterprise_token):
    """企业用户认证头"""
    return {'Authorization': f'Bearer {enterprise_token}'}


@pytest.fixture
def auth_headers_individual(individual_token):
    """个人用户认证头"""
    return {'Authorization': f'Bearer {individual_token}'}


@pytest.fixture
def sample_loan_data():
    """示例贷款申请数据"""
    return {
        'ent_name': '测试企业有限公司',
        'uscc': '91310115MA1K4QLX1L',
        'company_email': 'test@company.com',
        'company_address': '上海市浦东新区测试路123号',
        'repay_account_bank': 'ICBC',
        'repay_account_no': '1234567890123456789',
        'loan_amount': 1000000,
        'loan_term': '12',
        'loan_purpose': 'SECURED',
        'prop_proof_type': 'REAL_ESTATE',
        'industry_category': 'MANUFACTURING'
    }


@pytest.fixture
def loan_application(db, enterprise_user, sample_loan_data):
    """创建贷款申请记录"""
    loan = LoanApplication(
        user_id=enterprise_user.id,
        **sample_loan_data,
        prop_proof_docs_path='/uploads/test.pdf',
        status='PENDING'
    )
    db.session.add(loan)
    db.session.commit()
    return loan


@pytest.fixture
def mock_file():
    """模拟文件上传"""
    from io import BytesIO
    from werkzeug.datastructures import FileStorage
    
    return FileStorage(
        stream=BytesIO(b"test file content"),
        filename="test_document.pdf",
        content_type="application/pdf"
    )