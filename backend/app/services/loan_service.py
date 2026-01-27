"""
贷款申请相关的服务层
"""
from app.crud.loan_crud import (
    create_loan_application,
    get_financial_data
)
from app.models.user import EnterpriseLoanInfo
from werkzeug.datastructures import FileStorage
from flask import current_app
import os
from datetime import datetime


class LoanService:
    """贷款申请服务类"""
    
    @staticmethod
    def get_upload_folder() -> str:
        """
        获取上传文件夹路径，支持绝对路径和相对路径
        
        Returns:
            str: 上传文件夹的绝对路径
        """
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads/loan_docs')
        
        # 判断是否为绝对路径
        if os.path.isabs(upload_folder):
            # 绝对路径，直接使用
            return upload_folder
        else:
            # 相对路径，相对于项目根目录
            # 获取项目根目录（backend目录的上一级）
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            return os.path.join(project_root, upload_folder)
    
    @staticmethod
    def upload_file_only(file: FileStorage = None) -> dict:
        """
        只上传文件，不保存到数据库
        支持通过配置文件指定任意上传路径（绝对路径或相对路径）
        
        Args:
            file: 上传的文件
            
        Returns:
            dict: 文件信息
        """
        if not file or not file.filename:
            return {'file_path': None, 'file_name': None}
        
        # 获取配置的上传目录
        upload_folder = LoanService.get_upload_folder()
        
        # 创建上传目录（如果不存在）
        os.makedirs(upload_folder, exist_ok=True)
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(upload_folder, filename)
        
        # 保存文件
        file.save(filepath)
        
        # 统一使用正斜线，避免Windows系统的反斜线问题
        filepath_normalized = filepath.replace('\\', '/')
        
        return {
            'file_path': filepath_normalized,
            'file_name': file.filename
        }
    
    @staticmethod
    def save_to_database(loan_data: dict) -> EnterpriseLoanInfo:
        """
        保存贷款申请到数据库
        
        Args:
            loan_ 贷款申请数据
            
        Returns:
            EnterpriseLoanInfo: 创建的贷款申请对象
        """
        return create_loan_application(loan_data)
    
    @staticmethod
    def create_application(data: dict, file: FileStorage = None) -> EnterpriseLoanInfo:
        """
        创建贷款申请（旧方法，保留兼容性）
        
        Args:
             贷款申请数据
            file: 上传的文件
            
        Returns:
            EnterpriseLoanInfo: 创建的贷款申请对象
        """
        # 处理文件上传
        if file and file.filename:
            file_info = LoanService.upload_file_only(file)
            data['prop_proof_docs'] = file_info['file_path']
            data['prop_proof_docs_name'] = file_info['file_name']
        
        return create_loan_application(data)
    
    @staticmethod
    def get_chart_data() -> list:
        """
        获取图表数据（从JSON或模拟数据）
        
        Returns:
            list: 财务数据列表
        """
        return get_financial_data()
