from fastapi import APIRouter
from app.schemas.text import TextRequest, TranslationRequest, TextResponse
from app.services import conversion_service

router = APIRouter()


@router.post("/to-traditional", response_model=TextResponse)
def to_traditional(request: TextRequest):
    result = conversion_service.convert_to_traditional(request.content)
    return {"result": result}


@router.post("/to-simplified", response_model=TextResponse)
def to_simplified(request: TextRequest):
    result = conversion_service.convert_to_simplified(request.content)
    return {"result": result}


@router.post("/translate", response_model=TextResponse)
async def translate(request: TranslationRequest):
    result = await conversion_service.translate_text_async(request.content, request.target_lang)
    return {"result": result}


@router.post("/html-to-markdown", response_model=TextResponse)
def html_to_markdown(request: TextRequest):
    result = conversion_service.convert_html_to_markdown(request.content)
    return {"result": result}


# 这是要检查的代码块
@router.post("/sql-compress", response_model=TextResponse) # 检查点1：装饰器拼写和括号
def sql_compress(request: TextRequest):
    """
    接收格式化的SQL查询，并将其作为压缩后的单行返回。
    """
    compressed_result = conversion_service.compress_sql(request.content)
    return {"result": compressed_result}

@router.get("/ok")
def ok():
    return {"result": "ok"}

