# 1. 使用官方的 Python 3.11 slim 镜像作为基础镜像
FROM python:3.11-slim

# 2. 设置工作目录
WORKDIR /code

# ==================== 新增部分：安装 Node.js ====================
# 安装 Node.js 和 npm（Node.js 的包管理器）
# RUN apt-get update -y && apt-get install -y nodejs npm
# 官方的 Debian bookworm 源中的 nodejs 版本可能过旧，推荐使用 NodeSource 的源来安装较新版本
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs
# ===============================================================

# 3. 复制依赖文件并安装依赖
# 这一步会利用 Docker 的层缓存，只有在 requirements.txt 变化时才会重新安装
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. 复制应用代码到工作目录
COPY ./app /code/app

# 5. 暴露端口，让容器外的服务可以访问
EXPOSE 8000

# 6. 定义容器启动时要执行的命令
# 使用 uvicorn 启动 FastAPI 应用
# --host 0.0.0.0 使其可以从外部访问
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]