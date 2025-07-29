# Docker 部署指南

本指南将帮助您将 FastAPI 工具项目打包成 Docker 镜像并推送到 Docker Hub。

## 前置要求

1. 安装 Docker Desktop
2. 注册 Docker Hub 账号
3. 在本地登录 Docker Hub

```bash
docker login
```

## 快速开始

### 方法一：使用自动化脚本（推荐）

#### Windows 用户
```cmd
# 构建并推送镜像
build_and_push.bat <你的dockerhub用户名> <镜像名称> <标签>

# 例如：
build_and_push.bat myusername fastapi-tool-api latest
```

#### Linux/Mac 用户
```bash
# 给脚本执行权限
chmod +x build_and_push.sh

# 构建并推送镜像
./build_and_push.sh <你的dockerhub用户名> <镜像名称> <标签>

# 例如：
./build_and_push.sh myusername fastapi-tool-api latest
```

### 方法二：手动构建和推送

#### 1. 构建 Docker 镜像

```bash
# 构建镜像
docker build -t <你的dockerhub用户名>/<镜像名称>:<标签> .

# 例如：
docker build -t myusername/fastapi-tool-api:latest .
```

#### 2. 测试镜像

```bash
# 运行容器测试
docker run -p 8000:8000 <你的dockerhub用户名>/<镜像名称>:<标签>

# 例如：
docker run -p 8000:8000 myusername/fastapi-tool-api:latest
```

访问 http://localhost:8000 查看应用是否正常运行。

#### 3. 推送到 Docker Hub

```bash
# 推送镜像
docker push <你的dockerhub用户名>/<镜像名称>:<标签>

# 例如：
docker push myusername/fastapi-tool-api:latest
```

## 使用 Docker Compose

### 本地开发和测试

```bash
# 启动服务
docker-compose up --build

# 后台运行
docker-compose up -d --build

# 停止服务
docker-compose down
```

### 生产环境部署

1. 修改 `docker-compose.yml` 中的镜像名称为你推送到 Docker Hub 的镜像
2. 根据需要调整环境变量和端口配置
3. 运行：

```bash
docker-compose up -d
```

## 镜像优化说明

本项目的 Dockerfile 已经进行了以下优化：

1. **多阶段构建**：使用 Python 3.11 slim 镜像减小镜像大小
2. **层缓存优化**：先复制 requirements.txt 再安装依赖，提高构建效率
3. **安全性**：创建非 root 用户运行应用
4. **环境变量**：设置 Python 相关环境变量优化性能
5. **.dockerignore**：排除不必要的文件，减小构建上下文

## 环境变量配置

可以通过环境变量配置应用：

```bash
# 设置端口
docker run -p 8000:8000 -e PORT=8000 <镜像名称>

# 设置其他环境变量
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=info \
  <镜像名称>
```

## 健康检查

镜像包含健康检查配置，可以监控应用状态：

```bash
# 查看容器健康状态
docker ps

# 查看健康检查日志
docker inspect <容器ID> | grep Health -A 10
```

## 故障排除

### 常见问题

1. **构建失败**：检查 requirements.txt 中的依赖是否正确
2. **推送失败**：确保已登录 Docker Hub 且有推送权限
3. **运行失败**：检查端口是否被占用，查看容器日志

### 查看日志

```bash
# 查看容器日志
docker logs <容器ID>

# 实时查看日志
docker logs -f <容器ID>
```

### 进入容器调试

```bash
# 进入运行中的容器
docker exec -it <容器ID> /bin/bash
```

## 生产环境建议

1. 使用具体的版本标签而不是 `latest`
2. 设置资源限制
3. 配置日志收集
4. 使用 Docker Swarm 或 Kubernetes 进行编排
5. 定期更新基础镜像和依赖

## 示例部署命令

```bash
# 生产环境运行
docker run -d \
  --name fastapi-tool-api \
  --restart unless-stopped \
  -p 8000:8000 \
  --memory=512m \
  --cpus=1 \
  myusername/fastapi-tool-api:v1.0.0
```