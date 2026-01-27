from datetime import datetime
from app import db
import bcrypt


class User(db.Model):
    """用户模型 - 对应 user 表"""
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    user_name = db.Column(db.String(50), unique=True, nullable=False, index=True, comment='用户名')
    password = db.Column(db.String(100), nullable=False, comment='密码(加密后)')
    user_type = db.Column(db.String(20), nullable=False, comment='用户类型: INDIVIDUAL(个人) 或 ENTERPRISE(法人)')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment='更新时间'
    )

    def set_password(self, password_text):
        """设置密码 - 使用 bcrypt 加密"""
        password_bytes = password_text.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def check_password(self, password_text):
        """验证密码"""
        password_bytes = password_text.encode('utf-8')
        password_hash_bytes = self.password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_name': self.user_name,
            'user_type': self.user_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<User {self.user_name}>'


class EnterpriseLoanInfo(db.Model):
    """企业贷款信息模型 - 对应 enterprise_loan_info 表"""
    __tablename__ = 'enterprise_loan_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    ent_name = db.Column(db.String(200), nullable=False, comment='企业名称')
    uscc = db.Column(db.String(18), nullable=False, comment='统一社会信用代码')
    company_email = db.Column(db.String(200), nullable=False, comment='企业邮箱')
    company_address = db.Column(db.String(500), nullable=False, comment='企业地址')
    repay_account_bank = db.Column(db.String(50), nullable=False, comment='还款账户银行')
    repay_account_no = db.Column(db.String(19), nullable=False, comment='还款账户账号')
    loan_amount = db.Column(db.Numeric(15, 2), nullable=False, comment='贷款申请金额')
    loan_term = db.Column(db.String(20), nullable=False, comment='贷款期限')
    loan_purpose = db.Column(db.String(50), nullable=False, comment='贷款目的')
    prop_proof_type = db.Column(db.String(50), nullable=False, comment='财产证明类型')
    prop_proof_docs = db.Column(db.String(500), comment='财产证明文件路径')
    prop_proof_docs_name = db.Column(db.String(128), comment='财产证明文件名称')
    industry_category = db.Column(db.String(100), comment='所属行业')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment='更新时间'
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'ent_name': self.ent_name,
            'uscc': self.uscc,
            'company_email': self.company_email,
            'company_address': self.company_address,
            'repay_account_bank': self.repay_account_bank,
            'repay_account_no': self.repay_account_no,
            'loan_amount': float(self.loan_amount) if self.loan_amount else None,
            'loan_term': self.loan_term,
            'loan_purpose': self.loan_purpose,
            'prop_proof_type': self.prop_proof_type,
            'prop_proof_docs': self.prop_proof_docs,
            'prop_proof_docs_name': self.prop_proof_docs_name,
            'industry_category': self.industry_category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<EnterpriseLoanInfo {self.ent_name}>'