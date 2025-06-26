from fastapi import APIRouter
from app.services import external_service

router = APIRouter()

# @router.get("/call-joke-api")
# async def call_joke_api():
#     """预留的调用第三方API的示例，这里调用一个公共的笑话API"""
#     joke_api_url = "https://official-joke-api.appspot.com/random_joke"
#     data = await external_service.call_third_party_api(joke_api_url)
#     return data