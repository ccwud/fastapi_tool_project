import httpx

async def call_third_party_api(url: str):
    # 这是一个调用第三方API的示例
    # 使用 httpx 进行异步请求
    async with httpx.AsyncClient() as client:
        try:
            # 以一个公共API为例：获取随机笑话
            response = await client.get(url)
            response.raise_for_status()  # 如果响应状态码不是 2xx，则引发异常
            return response.json()
        except httpx.RequestError as exc:
            return {"error": f"An error occurred while requesting {exc.request.url!r}: {exc}"}