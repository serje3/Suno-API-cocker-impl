# -*- coding:utf-8 -*-

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import schemas
from utils import generate_lyrics, generate_music, get_feed, get_lyrics, get_credits, get_user_feed, PageQuery

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_scheme = HTTPBearer()


@app.get("/")
async def get_root():
    return schemas.Response()


@app.post("/generate")
async def generate(
        data: schemas.CustomModeGenerateParam, token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    try:
        resp = await generate_music(data.dict(), token.credentials)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.post("/generate/description-mode")
async def generate_with_song_description(
        data: schemas.DescriptionModeGenerateParam, token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    try:
        resp = await generate_music(data.dict(), token.credentials)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/feed/{aid}")
async def fetch_feed(aid: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        resp = await get_feed(aid, token.credentials)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/feed/")
async def fetch_user_feed(page: Annotated[int | None, PageQuery] = 0,
                          token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        resp = await get_user_feed(token.credentials, page or 0)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.post("/generate/lyrics/")
async def generate_lyrics_post(request: Request, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    req = await request.json()
    prompt = req.get("prompt")
    if prompt is None:
        raise HTTPException(
            detail="prompt is required", status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        resp = await generate_lyrics(prompt, token.credentials)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/lyrics/{lid}")
async def fetch_lyrics(lid: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        resp = await get_lyrics(lid, token.credentials)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/get_credits")
async def fetch_credits(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        resp = await get_credits(token.credentials)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
