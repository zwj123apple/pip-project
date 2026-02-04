# Jenkins CI/CD 配置指南

本文档详细说明如何配置Jenkins实现前后端项目的自动化测试和部署。

## 📋 目录

- [前置要求](#前置要求)
- [Jenkins安装与配置](#jenkins安装与配置)
- [项目配置](#项目配置)
- [Pipeline说明](#pipeline说明)
- [环境变量配置](#环境变量配置)
- [使用指南](#使用指南)
- [常见问题](#常见问题)

## 🔧 前置要求

### 服务器要求

- Jenkins 2.x 或更高版本
- Docker 20.10+ (用于容器化部署)
- Git
- 至少 4GB RAM
- 20GB 可用磁盘空间

### Jenkins插件

需要安装以下Jenkins插件:

**必需插件:**

- Pipeline (Workflow Aggregator)
- Git plugin
- Docker Pipeline
- JUnit Plugin
- Code Coverage API
- HTML Publisher

**推荐插件:**

- Blue Ocean (更好的UI)
- Email Extension Plugin (邮件通知)
- Slack Notification (Slack通知)
- Kubernetes (如果部署到K8s)
- Ansible (如果使用Ansible部署)

### 安装插件命令

```bash
# 通过Jenkins CLI安装插件
java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin \
  workflow-aggregator git docker-workflow junit \
  code-coverage-api htmlpublisher blueocean \
  email-ext slack kubernetes ansible
```

## 🚀 Jenkins安装与配置

### 1. 使用Docker安装Jenkins

```bash
# 创建Jenkins数据卷
docker volume create jenkins_home

# 运行Jenkins容器
docker run -d \
  --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

# 获取初始管理员密码
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 2. Jenkins初始配置

1. 访问 `http://localhost:8080`
2. 输入初始管理员密码
3. 安装推荐的插件
4. 创建管理员用户

### 3. 配置全局工具

**Jenkins -> 系统管理 -> 全局工具配置**

#### Python配置

```
名称: Python-3.9
安装方式: 自动安装
版本: 3.9
```

#### Node.js配置

```
名称: NodeJS-18
安装方式: 自动安装
版本: 18.x
```

#### Docker配置

```
名称: docker
安装方式: 已安装在宿主机
```

## 📦 项目配置

### 1. 创建Jenkins Pipeline任务

1. **新建任务**
   - 点击 "New Item"
   - 输入任务名称: `pip-project-pipeline`
   - 选择 "Pipeline"
   - 点击 "OK"

2. **配置Git仓库**

   在 "Pipeline" 部分:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/your-username/pip-project.git`
   - Credentials: 添加Git凭证
   - Branch: `*/main` (或其他分支)
   - Script Path: `Jenkinsfile`

3. **配置触发器**

   勾选以下选项:
   - ✅ GitHub hook trigger for GITScm polling (需要配置GitHub Webhook)
   - ✅ Poll SCM: `H/5 * * * *` (每5分钟检查一次,仅作为备份)

### 2. 配置凭证

**Jenkins -> 系统管理 -> 凭据管理**

#### Git凭证

```
类型: Username with password 或 SSH Username with private key
ID: git-credentials
描述: Git repository credentials
```

#### Docker Registry凭证

```
类型: Username with password
ID: docker-credentials-id
用户名: your-docker-username
密码: your-docker-password
描述: Docker Hub credentials
```

### 3. 配置环境变量

**Jenkins -> 系统管理 -> 系统配置 -> 全局属性**

勾选 "Environment variables" 并添加:

```
名称                    值
-----------------      ----------------------------------
DOCKER_REGISTRY        your-registry.com
DATABASE_URL          mysql://user:pass@host:3306/db
SECRET_KEY            your-secret-key-here
JWT_SECRET_KEY        your-jwt-secret-key-here
```

## 🔄 Pipeline说明

### Pipeline阶段详解

#### 1. Checkout (代码拉取)

- 从Git仓库拉取最新代码
- 获取git commit信息
- 显示当前分支和commit hash

#### 2. 环境准备 (并行)

- 后端环境: 安装Python依赖
- 前端环境: 安装Node.js依赖

#### 3. 代码质量检查 (并行)

- 后端: Pylint代码检查
- 前端: ESLint代码检查

#### 4. 单元测试 (并行)

- 后端: pytest测试 + 覆盖率报告
- 前端: vitest测试 + 覆盖率报告
- 发布JUnit测试报告和覆盖率报告

#### 5. 构建 (并行)

- 后端: 编译Python字节码
- 前端: 生产环境构建 (npm run build)

#### 6. Docker镜像构建 (仅main分支)

- 构建后端Docker镜像
- 构建前端Docker镜像
- 标记为latest和构建号

#### 7. 集成测试 (仅main分支)

- 使用docker-compose启动服务
- 运行集成测试
- 清理测试环境

#### 8. 推送镜像 (仅main分支)

- 推送Docker镜像到镜像仓库

#### 9. 部署 (仅main分支)

- 部署到生产环境
- 支持多种部署方式: SSH + Docker Compose、Kubernetes、Ansible

#### 10. 烟雾测试 (仅main分支)

- 检查部署后的服务健康状态
- 验证关键功能可用

### Pipeline流程图

```
┌─────────────┐
│  Checkout   │
└──────┬──────┘
       │
┌──────▼──────┐
│  环境准备    │ (并行)
└──────┬──────┘
       │
┌──────▼──────┐
│ 代码质量检查 │ (并行)
└──────┬──────┘
       │
┌──────▼──────┐
│  单元测试    │ (并行)
└──────┬──────┘
       │
┌──────▼──────┐
│    构建     │ (并行)
└──────┬──────┘
       │
┌──────▼──────┐
│ Docker镜像  │ (main分支)
└──────┬──────┘
       │
┌──────▼──────┐
│  集成测试    │ (main分支)
└──────┬──────┘
       │
┌──────▼──────┐
│  推送镜像    │ (main分支)
└──────┬──────┘
       │
┌──────▼──────┐
│    部署     │ (main分支)
└──────┬──────┘
       │
┌──────▼──────┐
│  烟雾测试    │
└─────────────┘
```

## 🔐 环境变量配置

### Backend环境变量

在 `.env` 文件或Jenkins环境变量中配置:

```bash
# Flask配置
FLASK_ENV=production
FLASK_APP=run.py

# 数据库
DATABASE_URL=mysql://username:password@host:3306/database

# 安全密钥
SECRET_KEY=your-very-long-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# JWT配置
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# 文件上传
UPLOAD_FOLDER=uploads/loan_docs
MAX_CONTENT_LENGTH=16777216
```

### Frontend环境变量

创建 `.env.production`:

```bash
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_TITLE=贷款申请系统
```

## 🎯 使用指南

### 触发构建

#### 1. 自动触发 (推荐)

```bash
# 提交代码到Git仓库
git add .
git commit -m "feat: add new feature"
git push origin main

# Jenkins会自动检测到变更并开始构建
```

#### 2. 手动触发

- 在Jenkins界面点击 "Build Now"

#### 3. 通过API触发

```bash
curl -X POST http://jenkins-url:8080/job/pip-project-pipeline/build \
  --user username:token
```

### 查看构建结果

1. **Pipeline视图**
   - 访问: http://jenkins-url:8080/job/pip-project-pipeline/
   - 查看各阶段执行状态

2. **Blue Ocean视图** (推荐)
   - 访问: http://jenkins-url:8080/blue/organizations/jenkins/pip-project-pipeline/
   - 更直观的可视化界面

3. **测试报告**
   - 点击构建号 -> Test Result
   - 查看单元测试通过率

4. **覆盖率报告**
   - 点击构建号 -> Code Coverage
   - 查看代码覆盖率详情

## 🐳 Docker部署

### 使用Docker Compose部署

```bash
# 1. 克隆代码
git clone https://github.com/your-username/pip-project.git
cd pip-project

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env 填入实际配置

# 3. 启动服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f

# 5. 停止服务
docker-compose down
```

## ❓ 常见问题

### 1. Python依赖安装失败

**问题**: `pip install` 超时或失败

**解决方案**:

```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. Node模块安装失败

**问题**: `npm install` 失败

**解决方案**:

```bash
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm ci
```

### 3. Docker权限问题

**问题**: `permission denied while trying to connect to Docker daemon`

**解决方案**:

```bash
# 将Jenkins用户添加到docker组
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 4. 测试覆盖率未达标

**问题**: 覆盖率低于90%导致构建失败

**解决方案**:

- 编写更多测试用例
- 或在pytest.ini中调整阈值: `--cov-fail-under=80`

### 5. 内存不足

**问题**: Jenkins构建时内存不足

**解决方案**:

```bash
# 增加Jenkins内存
export JENKINS_JAVA_OPTIONS="-Xmx2048m -Xms512m"
```

## 📚 更多资源

- [Jenkins官方文档](https://www.jenkins.io/doc/)
- [Jenkins Pipeline语法](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker文档](https://docs.docker.com/)
- [pytest文档](https://docs.pytest.org/)
- [Vitest文档](https://vitest.dev/)
