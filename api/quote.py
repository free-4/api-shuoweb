from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
import json
import random

router = APIRouter()

DATA_PATH = "./data/quote.json"

def load_quotes():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def pretty(data):
    return JSONResponse(content=data, media_type="application/json; charset=utf-8",
                        headers={"X-Content-Type-Options": "nosniff"})

# 随机返回一句名言
@router.get("/")
def get_random_quote(
    author: Optional[str] = Query(None, description="按作者筛选，如 鲁迅、爱因斯坦")
):
    quotes = load_quotes()
    if author:
        quotes = [q for q in quotes if q["author"] == author]
        if not quotes:
            raise HTTPException(status_code=404, detail=f"未找到作者 '{author}' 的句子")
    selected = random.choice(quotes)
    return pretty(selected)

# 获取全部句子（调试用）
@router.get("/all")
def get_all_quotes():
    quotes = load_quotes()
    return pretty({"total": len(quotes), "quotes": quotes})