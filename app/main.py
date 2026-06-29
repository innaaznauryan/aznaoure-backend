import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.data.product_seed import PRODUCTS_SEED
from app.database import Base, SessionLocal, engine
from app.models import Order, OrderItem, Product  # noqa: F401
from app.repositories.product_repository import ProductRepository
from app.routers import auth, orders, products, addresses

@asynccontextmanager
async def lifespan(_app: FastAPI):
    db = SessionLocal()
    try:
        ProductRepository(db).seed_if_empty(PRODUCTS_SEED)
    finally:
        db.close()
    yield

app = FastAPI(title="Jewelry Shop API", version="1.0.0", lifespan=lifespan)

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(addresses.router, prefix="/api/addresses", tags=["Addresses"])

@app.get("/")
def root():
    return {"message": "Jewelry Shop API is running 💍"}