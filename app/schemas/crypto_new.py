from pydantic import BaseModel, Field


class CryptoRequestNew(BaseModel):
    text: str
    key: str = Field(..., min_length=1, max_length=256, description="Encryption key with flexible length")


class CryptoResponseNew(BaseModel):
    result: str