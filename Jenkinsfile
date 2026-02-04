pipeline {
    agent any
    
    environment {
        // 环境变量配置
        BACKEND_DIR = 'backend'
        FRONTEND_DIR = 'frontend'
        PYTHON_VERSION = '3.9'
        NODE_VERSION = '18'
        
        // Docker镜像配置(如需要)
        DOCKER_REGISTRY = 'your-registry.com'
        BACKEND_IMAGE = "${DOCKER_REGISTRY}/pip-backend"
        FRONTEND_IMAGE = "${DOCKER_REGISTRY}/pip-frontend"
        IMAGE_TAG = "${BUILD_NUMBER}"
        
        // 测试报告路径
        BACKEND_TEST_REPORT = "${BACKEND_DIR}/test-reports"
        FRONTEND_TEST_REPORT = "${FRONTEND_DIR}/test-reports"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 拉取代码...'
                checkout scm
                
                script {
                    // 获取git信息
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                    env.GIT_BRANCH = sh(
                        script: "git rev-parse --abbrev-ref HEAD",
                        returnStdout: true
                    ).trim()
                }
                
                echo "分支: ${env.GIT_BRANCH}"
                echo "提交: ${env.GIT_COMMIT_SHORT}"
            }
        }
        
        stage('环境准备') {
            parallel {
                stage('后端环境') {
                    steps {
                        echo '🐍 准备Python环境...'
                        dir(BACKEND_DIR) {
                            sh '''
                                python --version
                                pip install --upgrade pip
                                pip install -r requirements.txt
                                pip install -r requirements-test.txt
                            '''
                        }
                    }
                }
                
                stage('前端环境') {
                    steps {
                        echo '📦 准备Node.js环境...'
                        dir(FRONTEND_DIR) {
                            sh '''
                                node --version
                                npm --version
                                npm ci
                            '''
                        }
                    }
                }
            }
        }
        
        stage('代码质量检查') {
            parallel {
                stage('后端代码检查') {
                    steps {
                        echo '🔍 后端代码质量检查...'
                        dir(BACKEND_DIR) {
                            sh '''
                                # Pylint检查
                                pylint app/ --output-format=text || true
                                
                                # 代码格式检查(可选)
                                # pip install black
                                # black --check app/ || true
                            '''
                        }
                    }
                }
                
                stage('前端代码检查') {
                    steps {
                        echo '🔍 前端代码质量检查...'
                        dir(FRONTEND_DIR) {
                            sh '''
                                # ESLint检查(如果配置了)
                                npm run lint || true
                            '''
                        }
                    }
                }
            }
        }
        
        stage('单元测试') {
            parallel {
                stage('后端测试') {
                    steps {
                        echo '🧪 运行后端测试...'
                        dir(BACKEND_DIR) {
                            sh '''
                                # 创建测试报告目录
                                mkdir -p test-reports
                                
                                # 运行pytest测试
                                pytest tests/ \
                                    --verbose \
                                    --cov=app \
                                    --cov-report=xml:test-reports/coverage.xml \
                                    --cov-report=html:test-reports/htmlcov \
                                    --junitxml=test-reports/junit.xml \
                                    || true
                            '''
                        }
                    }
                    post {
                        always {
                            // 发布测试报告
                            junit "${BACKEND_DIR}/test-reports/junit.xml"
                            
                            // 发布覆盖率报告
                            publishCoverage adapters: [
                                coberturaAdapter("${BACKEND_DIR}/test-reports/coverage.xml")
                            ]
                        }
                    }
                }
                
                stage('前端测试') {
                    steps {
                        echo '🧪 运行前端测试...'
                        dir(FRONTEND_DIR) {
                            sh '''
                                # 创建测试报告目录
                                mkdir -p test-reports
                                
                                # 运行Vitest测试
                                npm run test:ci || true
                            '''
                        }
                    }
                    post {
                        always {
                            // 发布前端测试报告(需要配置vitest生成junit格式)
                            junit "${FRONTEND_DIR}/test-reports/junit.xml"
                        }
                    }
                }
            }
        }
        
        stage('构建') {
            parallel {
                stage('后端构建') {
                    steps {
                        echo '🏗️ 构建后端...'
                        dir(BACKEND_DIR) {
                            sh '''
                                # 编译Python字节码
                                python -m compileall app/
                                
                                # 创建版本文件
                                echo "BUILD_NUMBER=${BUILD_NUMBER}" > version.txt
                                echo "GIT_COMMIT=${GIT_COMMIT_SHORT}" >> version.txt
                                echo "BUILD_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> version.txt
                            '''
                        }
                    }
                }
                
                stage('前端构建') {
                    steps {
                        echo '🏗️ 构建前端...'
                        dir(FRONTEND_DIR) {
                            sh '''
                                # 生产环境构建
                                npm run build
                                
                                # 创建版本文件
                                echo "BUILD_NUMBER=${BUILD_NUMBER}" > dist/version.txt
                                echo "GIT_COMMIT=${GIT_COMMIT_SHORT}" >> dist/version.txt
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Docker镜像构建') {
            when {
                branch 'main'  // 仅在main分支构建镜像
            }
            parallel {
                stage('后端镜像') {
                    steps {
                        echo '🐳 构建后端Docker镜像...'
                        dir(BACKEND_DIR) {
                            script {
                                docker.build("${BACKEND_IMAGE}:${IMAGE_TAG}")
                                docker.build("${BACKEND_IMAGE}:latest")
                            }
                        }
                    }
                }
                
                stage('前端镜像') {
                    steps {
                        echo '🐳 构建前端Docker镜像...'
                        dir(FRONTEND_DIR) {
                            script {
                                docker.build("${FRONTEND_IMAGE}:${IMAGE_TAG}")
                                docker.build("${FRONTEND_IMAGE}:latest")
                            }
                        }
                    }
                }
            }
        }
        
        stage('集成测试') {
            when {
                branch 'main'
            }
            steps {
                echo '🔗 运行集成测试...'
                sh '''
                    # 使用docker-compose启动服务
                    docker-compose -f docker-compose.test.yml up -d
                    
                    # 等待服务启动
                    sleep 10
                    
                    # 运行集成测试(如有)
                    # ./run-integration-tests.sh
                    
                    # 清理
                    docker-compose -f docker-compose.test.yml down
                '''
            }
        }
        
        stage('推送镜像') {
            when {
                branch 'main'
            }
            steps {
                echo '📤 推送Docker镜像到仓库...'
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials-id') {
                        docker.image("${BACKEND_IMAGE}:${IMAGE_TAG}").push()
                        docker.image("${BACKEND_IMAGE}:latest").push()
                        docker.image("${FRONTEND_IMAGE}:${IMAGE_TAG}").push()
                        docker.image("${FRONTEND_IMAGE}:latest").push()
                    }
                }
            }
        }
        
        stage('部署') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 部署到环境...'
                script {
                    // 根据分支决定部署环境
                    def environment = 'production'
                    
                    echo "部署到 ${environment} 环境"
                    
                    // 部署方式1: SSH到服务器执行部署脚本
                    // sh "ssh user@server 'cd /app && docker-compose pull && docker-compose up -d'"
                    
                    // 部署方式2: 使用Kubernetes
                    // sh "kubectl set image deployment/backend backend=${BACKEND_IMAGE}:${IMAGE_TAG}"
                    // sh "kubectl set image deployment/frontend frontend=${FRONTEND_IMAGE}:${IMAGE_TAG}"
                    
                    // 部署方式3: 使用Ansible
                    // ansiblePlaybook playbook: 'deploy.yml', inventory: 'production'
                }
            }
        }
        
        stage('烟雾测试') {
            when {
                branch 'main'
            }
            steps {
                echo '💨 运行烟雾测试...'
                sh '''
                    # 检查服务健康状态
                    curl -f http://your-backend-url/health || exit 1
                    curl -f http://your-frontend-url/ || exit 1
                    
                    echo "✅ 服务运行正常"
                '''
            }
        }
    }
    
    post {
        always {
            echo '📊 生成构建报告...'
            
            // 清理工作空间
            cleanWs(
                deleteDirs: true,
                patterns: [
                    [pattern: '**/node_modules/**', type: 'INCLUDE'],
                    [pattern: '**/__pycache__/**', type: 'INCLUDE'],
                    [pattern: '**/.pytest_cache/**', type: 'INCLUDE']
                ]
            )
        }
        
        success {
            echo '✅ 构建成功!'
            
            // 发送成功通知(可选)
            // emailext(
            //     subject: "✅ Jenkins构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            //     body: "构建成功完成!",
            //     to: "team@example.com"
            // )
        }
        
        failure {
            echo '❌ 构建失败!'
            
            // 发送失败通知(可选)
            // emailext(
            //     subject: "❌ Jenkins构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            //     body: "构建失败,请检查日志",
            //     to: "team@example.com"
            // )
        }
        
        unstable {
            echo '⚠️ 构建不稳定!'
        }
    }
}