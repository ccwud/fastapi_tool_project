from pydantic import BaseModel

class TextRequest(BaseModel):
    content: str

class TranslationRequest(BaseModel):
    content: str
    target_lang: str = 'en' # 默认为英文

class TextResponse(BaseModel):
    result: str