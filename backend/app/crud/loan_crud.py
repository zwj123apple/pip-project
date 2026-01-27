"""
贷款申请相关的CRUD操作
"""
from app import db
from app.models.user import EnterpriseLoanInfo


def create_loan_application(loan_data: dict) -> EnterpriseLoanInfo:
    """
    创建贷款申请
    
    Args:
        loan_ 贷款申请数据字典
        
    Returns:
        EnterpriseLoanInfo: 创建的贷款申请对象
    """
    loan = EnterpriseLoanInfo(**loan_data)
    db.session.add(loan)
    db.session.commit()
    db.session.refresh(loan)
    return loan


def get_financial_data() -> list:
    """
    获取财务数据（从JSON文件读取）
    用于确认页面的图表展示
    
    Returns:
        list: 财务数据列表
    """
    import json
    import os
    
    # 获取JSON文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, '..', '..', 'data', 'chart-data.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('financial_data', [])
    except FileNotFoundError:
        # 如果文件不存在，返回空列表
        return []
    except json.JSONDecodeError:
        # 如果JSON格式错误，返回空列表
        return []
