from typing import Any, Optional
from fastapi import APIRouter, Body, Depends, HTTPException

from app import core

import re


router = APIRouter()

@router.post("/des/encrypt/")
def encrypt(
    key: str = Body(...),
    message: str = Body(...),
    padding: bool = Body(...),
    initial: Optional[bytes] = None
) -> Any:
    try:
        key_obj = core.DesKey(str.encode(key))
        is_single = key_obj.is_single()
        is_triple = key_obj.is_triple()
        byte = key_obj.encrypt(message.encode('koi8_r'), initial=initial, padding=padding)
        return {"key": key_obj, "is_single": is_single, "is_triple": is_triple, "encrypted_message": str(byte, encoding='koi8_r')}
    except AssertionError as err:
        raise HTTPException(
            status_code=403,
            detail=f"{err}",
        )

@router.post("/des/decrypt/")
def decrypt(
    key: str = Body(...),
    encrypted_message: str = Body(...),
    padding: bool = Body(...),
) -> Any:
    try:
        key_obj = core.DesKey(str.encode(key))
        message = key_obj.decrypt(encrypted_message.encode('koi8_r'), padding=padding)

        return {"key": key, "message": message}
    except AssertionError as err:
        raise HTTPException(
            status_code=403,
            detail=f"{err}",
        )

@router.post("/wiegener/encrypt/")
def encrypt(
    key: str = Body(...),
    message: str = Body(...)
) -> Any:
    try:
        wiegener = core.Wiegener(key)
        encrypted_message = wiegener.encode_wiegener(message)
        return {"key": key, "encrypted_message": encrypted_message}
    except AssertionError as err:
        raise HTTPException(
            status_code=403,
            detail=f"{err}",
        )

@router.post("/wiegener/decrypt/")
def decrypt(
    key: str = Body(...),
    encrypted_message: str = Body(...)
) -> Any:
    try:
        wiegener = core.Wiegener(key)
        message = wiegener.decode_wiegener(encrypted_message)
        return {"key": key, "message": message}
    except AssertionError as err:
        raise HTTPException(
            status_code=403,
            detail=f"{err}",
        )
