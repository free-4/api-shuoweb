from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_summary():
    return {"total": 100, "data": []}