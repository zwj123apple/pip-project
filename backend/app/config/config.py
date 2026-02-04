import os
from datetime import timedelta


class Config:
    """应用配置类"""
    # MySQL 数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'loan_db')
    
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@'
        f'{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
        f'?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_size': 10,
        'max_overflow': 20
    }

    # JWT 配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    JWT_ALGORITHM = 'HS256'

    # 应用配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-app-secret-key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'

    # CORS 配置
    CORS_ORIGINS = ['http://localhost:5173']
    
    # 文件上传配置
    # 支持绝对路径或相对路径
    # 绝对路径示例: 'C:/uploads/loan_docs' 或 '/var/uploads/loan_docs'
    # 相对路径示例: 'uploads/loan_docs' (相对于项目根目录)
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/loan_docs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传文件大小: 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx'}


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
