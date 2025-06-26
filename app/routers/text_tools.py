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
def translate(request: TranslationRequest):
    result = conversion_service.translate_text_async(request.content, request.target_lang)
    return {"result": result}


@router.post("/html-to-markdown", response_model=TextResponse)
def html_to_markdown(request: TextRequest):
    result = conversion_service.convert_html_to_markdown(request.content)
    return {"result": result}


@router.post("/sql/compress", response_model=TextResponse, tags=["Text Tools"])
def sql_compress(request: TextRequest):
    """
    Accepts a formatted SQL query and returns it as a single, compressed line.
    """
    compressed_result = conversion_service.compress_sql(request.content)
    return {"result": compressed_result}