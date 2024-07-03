# -*- coding:utf-8 -*-
from typing import Annotated

from fastapi import Header, HTTPException



def get_token(authorization: Annotated[str | None, Header()] = None) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Отсутствует заголовок Authorization")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Неверный заголовок Authorization")
    token = authorization.split(' ')[1]
    # token = suno_auth.get_token()
    try:
        yield token
    finally:
        pass
