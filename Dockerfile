# 使用官方的 Python 3.11 slim 镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖和Node.js (translators包需要)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装依赖
# 这一步会利用 Docker 的层缓存，只有在 requirements.txt 变化时才会重新安装
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 复制应用代码到工作目录
COPY . .

# 创建非root用户
RUN adduser --disabled-password --gecos '' --shell /bin/bash user && \
    chown -R user:user /app
USER user

# 暴露端口，让容器外的服务可以访问
EXPOSE 8000

# 定义容器启动时要执行的命令
# 使用 uvicorn 启动 FastAPI 应用
# --host 0.0.0.0 使其可以从外部访问
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]