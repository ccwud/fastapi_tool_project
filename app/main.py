from fastapi import FastAPI
from .routers import text_tools, crypto_tools, external_apis

# 初始化 FastAPI 应用
app = FastAPI(
    title="My Awesome Tool API",
    description="A collection of useful tools provided as an API.",
    version="1.0.0",
)

# 注册各个功能的路由，并添加前缀以组织URL
app.include_router(text_tools.router, prefix="/api/v1/text", tags=["Text Tools"])
app.include_router(crypto_tools.router, prefix="/api/v1/crypto", tags=["Cryptography Tools"])
app.include_router(external_apis.router, prefix="/api/v1/external", tags=["External APIs"])


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Tool API! Visit /docs for documentation."}