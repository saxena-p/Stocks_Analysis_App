# from fastapi import FastAPI
# from app.api.routes import router

# app = FastAPI(
#     title="Stock Analysis MVP",
#     version="0.1.0",
#     description="Rank stocks by performance metrics"
# )

# app.include_router(router)

# @app.get("/")
# def health():
#     return {"status": "ok"}


from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.routes import router

app = FastAPI()
app.include_router(router)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})