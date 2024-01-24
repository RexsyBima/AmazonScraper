from pydantic import BaseModel


class Item(BaseModel):
    """
    Item basemodel, the data structure of amazon item products

    Keyword arguments:
    argument -- description
    Return: return_description
    """

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
    """
    the data structure of a sub category in categories. To be used in class Category

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    href: str | None = None
    name: str | None = None


class Category(BaseModel):
    """
    the data structure of category, has subcategory class values

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    category: str | None = None
    subcategory: Subcategory | None = Subcategory()


i = Item
