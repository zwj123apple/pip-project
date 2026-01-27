from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
import sys
import os
from app.config.config import config

db = SQLAlchemy()


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])
    
    # 设置JSON中文编码
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

    # 配置日志系统 - 输出到控制台
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # 配置根日志记录器
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ],
            force=True  # 强制重新配置
        )
        
        # 设置应用日志级别
        app.logger.setLevel(logging.DEBUG)
        
        # 确保所有应用模块的日志都输出
        for logger_name in ['app.api', 'app.services', 'app.crud', 'app.utils']:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
        
        app.logger.info("=" * 50)
        app.logger.info("应用启动 - 日志系统已配置")
        app.logger.info("=" * 50)

    # 初始化扩展
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

    # 注册蓝图
    from app.api.auth_controller import auth_bp
    from app.api.loan_controller import loan_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(loan_bp)

    return app
