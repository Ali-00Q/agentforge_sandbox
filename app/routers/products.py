from typing import Annotated
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["products"])


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float = Field(gt=0)


PRODUCTS: list[Product] = [
    Product(id=1, name="Laptop", description="High performance laptop", price=999.99),
    Product(id=2, name="Mouse", description="Wireless optical mouse", price=29.99),
    Product(id=3, name="Keyboard", description="Mechanical RGB keyboard", price=79.99),
]


@router.get("")
@router.get("/")
def list_products(
    search: Annotated[str | None, Query(description="Filter products by name")] = None,
) -> list[Product]:
    if search:
        search_lower = search.lower()
        return [p for p in PRODUCTS if search_lower in p.name.lower()]
    return PRODUCTS
