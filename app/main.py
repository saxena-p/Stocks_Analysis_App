from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Stock Analysis MVP",
    version="0.1.0",
    description="Rank stocks by performance metrics"
)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "ok"}