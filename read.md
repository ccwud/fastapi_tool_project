# FastAPI 工具集项目：部署与执行指南

本文档提供了在本地环境和使用 Docker 两种方式下运行此 FastAPI 项目的详细步骤。

## 1. 项目结构

在开始之前，请确保您的项目文件和目录结构如下：

```
fastapi_tool_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   └── routers/
│   │       ├── text_tools.py
│   │       ├── crypto_tools.py
│   │       └── external_apis.py
│   ├── schemas/
│   │   ├── crypto.py
│   │   └── text.py
│   └── services/
│       ├── conversion_service.py
│       ├── crypto_service.py
│       └── external_service.py
│
├── Dockerfile
├── .dockerignore
└── requirements.txt
```

---

## 2. 方法一：在本地环境运行 (推荐用于开发)

此方法利用 Python 虚拟环境在您的本地机器上直接运行应用，非常适合开发和调试。

### 先决条件

*   已安装 Python 3.11 或更高版本。
*   `pip` 和 `venv` 工具可用 (通常随 Python 一起安装)。

### 步骤

#### 第 1 步：创建并激活虚拟环境

在项目根目录 (`fastapi_tool_project/`) 打开终端，执行以下命令：

**对于 macOS / Linux:**
```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate
```
*成功激活后，你的终端提示符前会显示 `(.venv)`*

**对于 Windows (CMD / PowerShell):**
```powershell
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.\.venv\Scripts\activate
```
*成功激活后，你的终端提示符前会显示 `(.venv)`*


#### 第 2 步：安装项目依赖

确保你的虚拟环境已激活，然后运行以下命令来安装 `requirements.txt` 文件中列出的所有库：
```bash
pip install -r requirements.txt
```

#### 第 3 步：启动 FastAPI 应用

一切就绪后，使用 `uvicorn` 来启动应用服务器：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
**命令解析:**
- `app.main:app`: 指示 uvicorn 运行 `app` 文件夹下 `main.py` 文件中的 `app` 实例。
- `--reload`: 开启热重载。当你的代码文件被修改并保存时，服务器会自动重启，这在开发时非常方便。
- `--host 0.0.0.0`: 使应用可以被局域网内的其他设备访问。
- `--port 8000`: 指定服务运行在 8000 端口。

#### 第 4 步：访问应用

打开你的浏览器，访问以下地址：
- **API 交互文档 (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **应用根路径:** [http://localhost:8000/](http://localhost:8000/)

你可以直接在 `/docs` 页面测试所有 API 功能。

---

## 3. 方法二：使用 Docker 部署 (推荐用于生产)

此方法将应用打包成一个独立的 Docker 镜像，确保了环境的一致性，便于移植和部署。

### 先决条件

*   已安装并正在运行 Docker Desktop (Windows/macOS) 或 Docker Engine (Linux)。

### 步骤

#### 第 1 步：构建 Docker 镜像

在项目根目录 (`fastapi_tool_project/`) 打开终端，确保 `Dockerfile` 文件在此目录下。然后运行以下命令构建镜像：
```bash
docker build -t fastapi-tool-api .
```
**命令解析:**
- `docker build`: Docker 的构建命令。
- `-t fastapi-tool-api`: 为你的镜像打上一个标签（tag），名字叫 `fastapi-tool-api`。
- `.`: 表示 Docker 的构建上下文为当前目录。Docker 会查找当前目录下的 `Dockerfile` 来执行构建。

#### 第 2 步：运行 Docker 容器

镜像构建成功后，使用以下命令从该镜像启动一个容器：
```bash
docker run -d --name my-tool-api-container -p 8000:8000 fastapi-tool-api
```
**命令解析:**
- `docker run`: Docker 的运行命令。
- `-d`: (detached) 在后台运行容器。
- `--name my-tool-api-container`: 为运行的容器指定一个名字，方便后续管理。
- `-p 8000:8000`: 将你主机的 8000 端口映射到容器内部的 8000 端口。
- `fastapi-tool-api`: 要使用的镜像名称。

#### 第 3 步：管理和访问容器

*   **访问应用**: 与本地运行一样，在浏览器中打开 [http://localhost:8000/docs](http://localhost:8000/docs)。
*   **查看正在运行的容器**:
    ```bash
    docker ps
    ```
*   **查看容器日志**:
    ```bash
    docker logs my-tool-api-container
    ```
*   **停止容器**:
    ```bash
    docker stop my-tool-api-container
    ```
*   **移除已停止的容器**:
    ```bash
    docker rm my-tool-api-container
    ```