from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import json
import os
import random

router = APIRouter()

DATA_PATH = os.path.join(os.path.dirname(__file__), "./data/phone.json")

def load_phones():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 随机返回一个手机型号
@router.get("/")
def get_random_phone():
    phones = load_phones()
    return random.choice(phones)

# 按品牌或系统随机返回一个
@router.get("/search")
def search_random_phone(
    brand: Optional[str] = Query(None, description="按品牌筛选，如 Apple、Samsung"),
    os: Optional[str] = Query(None, description="按系统筛选，如 iOS、Android")
):
    phones = load_phones()
    if brand:
        phones = [p for p in phones if p["brand"].lower() == brand.lower()]
    if os:
        phones = [p for p in phones if p["os"].lower() == os.lower()]
    if not phones:
        raise HTTPException(status_code=404, detail="No matching phones found")
    return random.choice(phones)

# 获取全部列表（备用）
@router.get("/all")
def get_all_phones():
    phones = load_phones()
    return {"total": len(phones), "phones": phones}

# 按型号查单个
@router.get("/{model}")
def get_phone_by_model(model: str):
    phones = load_phones()
    model_clean = model.lower().replace("-", " ")
    for phone in phones:
        if phone["model"].lower() == model_clean:
            return phone
    raise HTTPException(status_code=404, detail=f"Phone '{model}' not found")
