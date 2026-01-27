"""
贷款申请模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.models import Base


class LoanApplication(Base):
    """企业贷款申请模型"""
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 基本信息
    ent_name = Column(String(200), nullable=False, comment="企业名称")
    uscc = Column(String(18), nullable=False, comment="统一社会信用代码")
    company_email = Column(String(100), nullable=False, comment="企业邮箱")
    company_address = Column(String(500), comment="企业地址")
    repay_account_bank = Column(String(100), nullable=False, comment="还款账户银行")
    repay_account_no = Column(String(19), nullable=False, comment="还款账户号码")
    
    # 贷款信息
    loan_amount = Column(Float, nullable=False, comment="贷款申请金额")
    loan_term = Column(String(50), nullable=False, comment="期限")
    loan_purpose = Column(String(50), nullable=False, comment="贷款目的")
    prop_proof_type = Column(String(50), nullable=False, comment="财产证明类型")
    prop_proof_docs = Column(String(500), comment="财产证明文件路径")
    industry_category = Column(String(50), comment="所属行业")
    
    # 状态和时间
    status = Column(String(20), default="pending", comment="申请状态")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="loan_applications")

    def __repr__(self):
        return f"<LoanApplication {self.id} - {self.ent_name}>"
