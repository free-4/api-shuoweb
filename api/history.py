from fastapi import APIRouter, HTTPException
from datetime import datetime
import json

router = APIRouter()

DATA_PATH = "./data/history.json"

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/")
def get_today():
    today = datetime.now().strftime("%m-%d")
    data = load_data()
    result = data.get(today)
    if not result:
        raise HTTPException(status_code=404, detail="暂无今天的历史事件")
    return {"date": today, "events": result}

@router.get("/{date}")
def get_by_date(date: str):
    # 支持 MM-DD 格式，如 01-10
    try:
        datetime.strptime(date, "%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 MM-DD 格式，如 01-10")
    data = load_data()
    result = data.get(date)
    if not result:
        raise HTTPException(status_code=404, detail=f"{date} 暂无历史事件记录")
    return {"date": date, "events": result}
