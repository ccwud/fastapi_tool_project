from pydantic import BaseModel, Field

class CryptoRequest(BaseModel):
    text: str
    key: str = Field(..., min_length=8, max_length=8, description="DES key must be 8 bytes long.")

class CryptoResponse(BaseModel):
    result: str