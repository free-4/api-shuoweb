from fastapi import APIRouter, HTTPException
import json

router = APIRouter()

DATA_PATH = "./data/number.json"

def load_data():
    data_dict = {}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            data_list = json.load(f)
            if isinstance(data_list, list):
                for item in data_list:
                    data_dict[item["_id"]] = item
        except json.JSONDecodeError:
            f.seek(0)
            for line in f:
                line = line.strip()
                if line:
                    item = json.loads(line)
                    data_dict[item["_id"]] = item
    return data_dict

def query_number(phone: str):
    phone = phone.strip()
    if not phone.isdigit() or len(phone) != 11:
        raise HTTPException(status_code=400, detail="请输入有效的11位纯数字手机号码")
    if phone.startswith("19"):
        raise HTTPException(status_code=400, detail="系统暂不支持查询以19开头的手机号码")
    data_dict = load_data()
    result = data_dict.get(phone[:7])
    if not result:
        raise HTTPException(status_code=404, detail="数据库中未找到该手机号的归属地信息")
    return result

@router.get("/")
def get_number(phone: str):
    return query_number(phone)