"""
贷款申请相关的API控制器
"""
from flask import Blueprint, request
from app.services.loan_service import LoanService
from app.utils.jwt_utils import token_required
from app.utils.response import ApiResponse
from pydantic import ValidationError
from app.schemas.loan_schema import LoanApplicationCreate


# 创建蓝图
loan_bp = Blueprint('loan', __name__, url_prefix='/api/loan')


def format_validation_errors(validation_errors):
    """
    格式化Pydantic验证错误列表
    
    :param validation_errors: Pydantic ValidationError的errors()列表
    :return: 格式化后的错误列表
    """
    formatted_errors = []
    
    for error in validation_errors:
        field = error['loc'][-1] if error['loc'] else 'unknown'
        error_type = error['type']
        
        # 自定义中文错误消息
        if 'missing' in error_type:
            msg = f'{field} 字段不能为空'
        elif 'string_type' in error_type:
            msg = f'{field} 必须是文本类型'
        elif 'float_type' in error_type or 'int_type' in error_type:
            msg = f'{field} 必须是数字'
        elif 'greater_than' in error_type or 'greater_than_equal' in error_type:
            msg = f'{field} 不能为负数'
        elif 'string_too_short' in error_type or 'string_too_long' in error_type:
            msg = f'{field} 长度不符合要求'
        else:
            msg = error['msg']
        
        formatted_errors.append({
            'field': field,
            'msg': msg,
            'type': error_type
        })
    
    return formatted_errors


def validate_business_rules(loan_data):
    """
    验证业务逻辑规则（贷款目的与期限的相关性检查）
    
    :param loan_ LoanApplicationCreate对象
    :return: 错误列表，如果没有错误则返回空列表
    """
    errors = []
    
    loan_purpose = loan_data.loan_purpose
    loan_term = float(loan_data.loan_term)
    
    # 信用贷款期限检查：不超过5年
    if loan_purpose == 'credit' and loan_term > 5:
        errors.append({
            'field': 'loan_term',
            'msg': '信用贷款期限不能超过5年',
            'type': 'business_rule'
        })
    
    # 税贷期限检查：不超过2年
    if loan_purpose == 'tax' and loan_term > 2:
        errors.append({
            'field': 'loan_term',
            'msg': '税贷期限不能超过2年',
            'type': 'business_rule'
        })
    
    return errors


def validate_loan_data(data):
    """
    统一的数据校验方法（Pydantic验证 + 业务规则验证）
    
    :param data: 表单数据字典
    :return: (loan_data, errors) - 如果验证成功返回(loan_data对象, None)，否则返回(None, 错误列表)
    """
    # 1. Pydantic基础验证
    try:
        loan_data = LoanApplicationCreate(**data)
    except ValidationError as e:
        # 格式化Pydantic验证错误
        formatted_errors = format_validation_errors(e.errors())
        return None, formatted_errors
    
    # 2. 业务规则验证
    business_errors = validate_business_rules(loan_data)
    if business_errors:
        return None, business_errors
    
    # 验证通过
    return loan_data, None


@loan_bp.route('/apply', methods=['POST'])
@token_required
def validate_and_upload():
    """
    验证数据并上传文件（不保存到数据库）
    同时返回财务图表数据
    
    需要认证
    """
    try:
        # 1. 获取表单数据
        data = request.form.to_dict()
        
        # 2. 添加文件占位符以通过Pydantic验证（先验证表单数据）
        data['prop_proof_docs'] = 'temp_file_path'
        data['prop_proof_docs_name'] = 'temp_filename'
        
        # 3. 先验证表单数据（Pydantic验证 + 业务规则验证）
        loan_data, errors = validate_loan_data(data)
        if errors:
            return ApiResponse.validation_error('数据验证失败，请检查输入信息', errors)
        
        # 4. 表单验证通过后，再检查文件是否上传
        file = request.files.get('prop_proof_docs')
        if not file or not file.filename:
            return ApiResponse.file_error('请上传财产证明文件')
        
        # 5. 上传文件
        try:
            file_info = LoanService.upload_file_only(file)
        except Exception as file_error:
            return ApiResponse.file_error(f'文件上传失败: {str(file_error)}')
        
        # 6. 获取财务图表数据
        financial_data = LoanService.get_chart_data()
        
        return ApiResponse.success(
            data={
                'loan_data': loan_data.model_dump(),
                'file_info': file_info,
                'financial_data': financial_data
            },
            msg='数据验证成功，请在下一步确认您的贷款申请信息'
        )
        
    except Exception as e:
        return ApiResponse.server_error(f'服务器错误: {str(e)}')


@loan_bp.route('/confirm', methods=['POST'])
@token_required
def confirm_loan():
    """
    确认并保存贷款申请到数据库
    
    需要认证
    """
    try:
        # 获取表单数据
        data = request.form.to_dict()
        
        # 统一的数据校验（Pydantic验证 + 业务规则验证）
        loan_data, errors = validate_loan_data(data)
        if errors:
            return ApiResponse.validation_error('数据验证失败，请检查输入信息', errors)
        
        # 保存到数据库
        loan_dict = loan_data.model_dump()
            
        loan = LoanService.save_to_database(loan_dict)
        
        return ApiResponse.success(
            data=loan.to_dict(),
            msg='贷款申请提交成功'
        )
        
    except Exception as e:
        return ApiResponse.server_error(f'服务器错误: {str(e)}')
