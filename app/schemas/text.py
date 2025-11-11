from pydantic import BaseModel

class TextRequest(BaseModel):
    content: str

class TranslationRequest(BaseModel):
    content: str
    target_lang: str = 'en' # 默认为英文

class TextResponse(BaseModel):
    result: str


class ApiDocsJsonRequest(BaseModel):
    """承载接口文档 JSON 的请求模型。
    传入字段 data 为整个文档的 JSON 对象。
    """
    data: dict