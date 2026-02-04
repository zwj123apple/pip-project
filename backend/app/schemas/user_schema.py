from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class UserLoginSchema(BaseModel):
    """用户登录模型"""
    user_name: str
    password: str

    @field_validator('user_name')
    @classmethod
    def validate_username(cls, v):
       # 先去除前后空格（用户名常见需求，避免全空格通过）
        if v is not None:
            v = v.strip()
        
        # 必须输入（不能为空）
        if not v:
            raise ValueError('用户名必须输入')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not v:
            raise ValueError('密码必须输入')
        if len(v)  != 8:
            raise ValueError('密码长度必须为8位')
        return v


class UserResponseSchema(BaseModel):
    """用户响应模型"""
    id: int
    user_name: str
    user_type: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginResponseSchema(BaseModel):
    """登录响应模型"""
    access_token: str
    user: UserResponseSchema