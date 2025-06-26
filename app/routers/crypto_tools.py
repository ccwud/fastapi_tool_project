from fastapi import APIRouter, HTTPException
from app.schemas.crypto import CryptoRequest, CryptoResponse
from app.services import crypto_service

router = APIRouter()


@router.post("/des/encrypt", response_model=CryptoResponse)
def des_encrypt(request: CryptoRequest):
    result = crypto_service.encrypt_des(request.text, request.key)
    return {"result": result}


@router.post("/des/decrypt", response_model=CryptoResponse)
def des_decrypt(request: CryptoRequest):
    try:
        result = crypto_service.decrypt_des(request.text, request.key)
        return {"result": result}
    except Exception:
        # 如果密钥错误或填充不正确，解密会失败
        raise HTTPException(status_code=400, detail="Decryption failed. Invalid key or data.")