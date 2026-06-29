from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    desc: str
    quantity: int
    price: float