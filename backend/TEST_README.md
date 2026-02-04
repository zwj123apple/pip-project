# Python后端单元测试文档

## 测试框架

本项目使用以下测试工具：

- **pytest**: Python测试框架
- **pytest-cov**: 代码覆盖率工具
- **pytest-mock**: Mock工具
- **pytest-flask**: Flask应用测试工具
- **faker**: 生成测试数据
- **factory-boy**: 创建测试fixtures

## 安装测试依赖

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-test.txt
```

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_api_auth.py
pytest tests/test_api_loan.py
```

### 运行特定测试类

```bash
pytest tests/test_api_auth.py::TestAuthLogin
```

### 运行特定测试方法

```bash
pytest tests/test_api_auth.py::TestAuthLogin::test_login_success
```

### 生成覆盖率报告

```bash
# 终端输出
pytest --cov=app

# 生成HTML报告
pytest --cov=app --cov-report=html

# 生成XML报告（用于CI/CD）
pytest --cov=app --cov-report=xml
```

### 查看详细输出

```bash
pytest -v -s
```

### 只运行标记的测试

```bash
# 只运行API测试
pytest -m api

# 只运行单元测试
pytest -m unit
```

## 测试文件结构

```
backend/tests/
├── __init__.py                    # 测试包初始化
├── conftest.py                    # pytest配置和fixtures
├── test_api_auth.py              # 认证API测试
├── test_api_loan.py              # 贷款API测试
├── test_services.py              # Service层测试
└── test_utils.py                 # 工具函数测试
```

## 测试覆盖范围

### API接口测试（100%覆盖）

#### 认证接口 (`/api/auth`)

- ✅ POST `/api/auth/login` - 用户登录
  - 成功登录
  - 错误密码
  - 用户不存在
  - 缺少必填字段
- ✅ POST `/api/auth/logout` - 用户退出
  - 成功退出
  - 无token退出
  - 无效token
- ✅ GET `/api/auth/test` - Token验证
  - 有效token
  - 无效token
  - 缺少token
  - 格式错误的Authorization头

#### 贷款接口 (`/api/loan`)

- ✅ POST `/api/loan/apply` - 贷款申请
  - 成功提交（带文件）
  - 未登录提交
  - 未上传文件
  - 缺少必填字段
  - 无效USCC
  - 无效邮箱
  - 无效银行账号
  - 负数贷款金额
  - 信用贷款超期限
  - 税贷超期限
- ✅ POST `/api/loan/confirm` - 贷款确认
  - 成功确认
  - 未登录确认
  - 缺少字段

### Service层测试

- ✅ AuthService - 认证服务
  - 登录成功
  - 错误密码
  - 用户不存在
  - 获取用户信息
- ✅ LoanService - 贷款服务
  - 文件上传
  - 保存到数据库
  - 获取图表数据

### 工具函数测试

- ✅ JWT工具
  - 创建token
  - 解码token
  - 无效token
  - 过期token
- ✅ API响应工具
  - 成功响应
  - 错误响应
  - 验证错误
  - 认证错误
  - 服务器错误
  - 文件错误
- ✅ 自定义异常
  - UnauthorizedException
  - BadRequestException
  - ForbiddenException

## GitHub Actions 集成

项目已配置 GitHub Actions 工作流，在以下情况自动运行测试：

- 推送到 `main` 或 `develop` 分支
- 提交 Pull Request 到 `main` 或 `develop` 分支
- 修改 `backend/` 目录下的文件

工作流配置文件：`.github/workflows/backend-test.yml`

### 工作流功能

- 在 Python 3.9, 3.10, 3.11 上运行测试
- 生成代码覆盖率报告
- 上传覆盖率报告到 Codecov
- 上传HTML覆盖率报告为artifact

## Fixtures说明

### 数据库Fixtures

- `app`: Flask应用实例（session级别）
- `db`: 数据库实例（function级别，每个测试后回滚）
- `client`: 测试客户端
- `runner`: CLI测试runner

### 用户Fixtures

- `enterprise_user`: 企业用户
- `individual_user`: 个人用户
- `enterprise_token`: 企业用户JWT token
- `individual_token`: 个人用户JWT token
- `auth_headers_enterprise`: 企业用户认证头
- `auth_headers_individual`: 个人用户认证头

### 数据Fixtures

- `sample_loan_data`: 示例贷款申请数据
- `loan_application`: 贷款申请记录
- `mock_file`: 模拟文件上传

## 测试编写指南

### 基本测试结构

```python
import pytest

class TestYourFeature:
    """测试你的功能"""

    def test_something(self, client, db):
        """测试某个功能"""
        # 准备数据
        data = {'key': 'value'}

        # 执行请求
        response = client.post('/api/endpoint', json=data)

        # 断言结果
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['code'] == 0
```

### 测试API接口

```python
def test_api_endpoint(self, client, auth_headers_enterprise):
    """测试API端点"""
    response = client.post(
        '/api/endpoint',
        json={'data': 'value'},
        headers=auth_headers_enterprise
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['code'] == 0
```

### 测试异常情况

```python
def test_exception_handling(self, client):
    """测试异常处理"""
    from app.utils.exceptions import BadRequestException

    with pytest.raises(BadRequestException):
        # 触发异常的代码
        raise BadRequestException('错误消息')
```

### Mock外部依赖

```python
def test_with_mock(self, mocker):
    """使用mock测试"""
    # Mock一个函数
    mock_function = mocker.patch('app.services.some_function')
    mock_function.return_value = 'mocked_value'

    # 执行测试
    result = some_function()
    assert result == 'mocked_value'
```

## 测试覆盖率目标

- ✅ **接口覆盖率**: 100%
- ✅ **分支覆盖率**: >90%
- ✅ **整体覆盖率**: >90%

## 持续改进

### 待添加的测试

- 更多的边界情况测试
- 性能测试
- 压力测试
- E2E测试

## 常见问题

### 1. 数据库连接问题

测试使用内存数据库（SQLite），无需配置MySQL。

### 2. Token过期问题

测试中的token不会过期
