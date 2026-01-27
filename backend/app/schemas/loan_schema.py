"""
贷款申请相关的Schema定义
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class LoanApplicationCreate(BaseModel):
    """创建贷款申请的Schema"""
    # 基本信息
    ent_name: str = Field(..., min_length=1, description="企业名称")
    uscc: str = Field(..., min_length=18, max_length=18, description="统一社会信用代码")
    company_email: str = Field(..., min_length=1, description="企业邮箱")
    company_address: Optional[str] = Field(None, description="企业地址")
    repay_account_bank: str = Field(..., min_length=1, description="还款账户银行")
    repay_account_no: str = Field(..., min_length=19, max_length=19, description="还款账户号码")

    # 贷款信息
    loan_amount: float = Field(..., gt=0, description="贷款申请金额")
    loan_term: str = Field(..., min_length=1, description="期限")
    loan_purpose: str = Field(..., min_length=1, description="贷款目的")
    prop_proof_type: str = Field(..., min_length=1, description="财产证明类型")
    prop_proof_docs: str = Field(..., min_length=1, description="财产证明文件路径")
    prop_proof_docs_name: str = Field(..., min_length=1, description="财产证明文件名称")
    industry_category: Optional[str] = Field(None, description="所属行业")

    @field_validator('ent_name', 'repay_account_bank', 'loan_term', 
                     'loan_purpose', 'prop_proof_type', 'prop_proof_docs', 
                     'prop_proof_docs_name')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """验证字段不能为空"""
        if not v or not v.strip():
            raise ValueError('此字段不能为空')
        return v.strip()

    @field_validator('uscc')
    @classmethod
    def validate_uscc(cls, v: str) -> str:
        """验证统一社会信用代码格式"""
        v = v.strip()
        if not v:
            raise ValueError('统一社会信用代码不能为空')
        if not re.match(r'^[0-9A-Za-z]{18}$', v):
            raise ValueError('统一社会信用代码必须是18位英数字')
        return v

    @field_validator('company_email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """验证邮箱格式"""
        v = v.strip()
        if not v:
            raise ValueError('企业邮箱不能为空')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('请输入有效的邮箱地址')
        return v

    @field_validator('repay_account_no')
    @classmethod
    def validate_account_no(cls, v: str) -> str:
        """验证账户号码格式"""
        v = v.strip()
        if not v:
            raise ValueError('还款账户号码不能为空')
        if not re.match(r'^\d{19}$', v):
            raise ValueError('还款账户号码必须是19位数字')
        return v

    @field_validator('loan_amount')
    @classmethod
    def validate_loan_amount(cls, v: float) -> float:
        """验证贷款金额"""
        if v <= 0:
            raise ValueError('贷款申请金额必须大于0')
        return v

    class Config:
        from_attributes = True


class LoanApplicationResponse(BaseModel):
    """贷款申请响应Schema"""
    id: int
    ent_name: str
    uscc: str
    company_email: str
    company_address: Optional[str]
    repay_account_bank: str
    repay_account_no: str
    loan_amount: float
    loan_term: str
    loan_purpose: str
    prop_proof_type: str
    prop_proof_docs: Optional[str]
    prop_proof_docs_name: Optional[str]
    industry_category: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class FinancialData(BaseModel):
    """财务数据Schema - 用于图表展示"""
    period: str = Field(..., description="财务期")
    profit: int = Field(..., description="利润")
    yoy: Optional[str] = Field(None, description="同比")
    qoq: Optional[str] = Field(None, description="环比")

    class Config:
        from_attributes = True
