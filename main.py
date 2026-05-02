from fastapi import FastAPI
from routers import summary, items

app = FastAPI()

app.include_router(summary.router, prefix="/summary", tags=["summary"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
def root():
    return {"message": "API is running"}