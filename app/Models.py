from pydantic import BaseModel


class Item(BaseModel):
    url: str | None = None
    title: str | None = None
    price: int | None = None
    decimal_price: int | None = None
    shipping: int | None = None
    category_price: list | None = None
    category: list | None = None
    total_rating: int | None = None
    rating: int | None = None
    features: list | None = None
    seller: str | None = None
    brand: str | None = None
    details: dict | None = None
    img_url: str | None = None


class Subcategory(BaseModel):
    href: str | None = None
    name: str | None = None


class Category(BaseModel):
    category: str | None = None
    subcategory: Subcategory | None = Subcategory()
