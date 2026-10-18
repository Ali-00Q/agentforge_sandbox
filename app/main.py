from fastapi import FastAPI
from app.routers.products import router as products_router

app = FastAPI(title="Product API")

app.include_router(products_router)


@app.get("/")
def read_root():
    return {"message": "API is running"}
