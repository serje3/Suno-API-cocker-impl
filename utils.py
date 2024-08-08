import json
import os
import time

import aiohttp
from aiohttp import BasicAuth
from dotenv import load_dotenv
from fastapi import Query

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

COMMON_HEADERS = {
    "Content-Type": "text/plain;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Referer": "https://suno.com",
    "Origin": "https://suno.com",
}

PageQuery = Query(ge=0)


async def fetch(url, headers=None, data=None, method="POST"):
    if headers is None:
        headers = {}
    headers.update(COMMON_HEADERS)
    if data is not None:
        data = json.dumps(data)

    headers_for_print = {**headers}
    headers_for_print['Authorization'] = f"Bearer *******"

    print(data, method, headers_for_print, url)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                    method=method, url=url, data=data, headers=headers, proxy=os.getenv("PROXY_URL"),
                    proxy_auth=BasicAuth(os.getenv("PROXY_USER"), os.getenv("PROXY_PASS")),
            ) as resp:
                return await resp.json()
        except Exception as e:
            return f"An error occurred: {e}"


async def get_feed(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/feed/?ids={ids}"
    response = await fetch(api_url, headers, method="GET")
    return response


async def get_user_feed(token: str, page: int = 0):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/feed?page={page}"
    response = await fetch(api_url, headers, method="GET")
    return response


async def generate_music(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/v2/"
    response = await fetch(api_url, headers, data)
    return response


async def generate_lyrics(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/"
    data = {"prompt": prompt}
    return await fetch(api_url, headers, data)


async def get_lyrics(lid, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/{lid}"
    return await fetch(api_url, headers, method="GET")


async def get_credits(token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/billing/info/"
    respose = await fetch(api_url, headers, method="GET")
    return {
        "credits_left": respose['total_credits_left'],
        "period": respose['period'],
        "monthly_limit": respose['monthly_limit'],
        "monthly_usage": respose['monthly_usage']
    }
