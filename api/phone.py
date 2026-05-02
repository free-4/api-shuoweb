from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import json
import os

router = APIRouter()

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/phone.json")

def load_phones():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/")
def get_all_phones():
    phones = load_phones()
    return {"total": len(phones), "phones": phones}

@router.get("/search")
def search_phones(
    brand: Optional[str] = Query(None, description="按品牌筛选，如 Apple、Samsung"),
    os: Optional[str] = Query(None, description="按系统筛选，如 iOS、Android")
):
    phones = load_phones()
    if brand:
        phones = [p for p in phones if p["brand"].lower() == brand.lower()]
    if os:
        phones = [p for p in phones if p["os"].lower() == os.lower()]
    return {"total": len(phones), "phones": phones}

@router.get("/{model}")
def get_phone_by_model(model: str):
    phones = load_phones()
    model_clean = model.lower().replace("-", " ")
    for phone in phones:
        if phone["model"].lower() == model_clean:
            return phone
    raise HTTPException(status_code=404, detail=f"Phone '{model}' not found")
