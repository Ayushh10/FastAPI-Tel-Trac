from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    describe: str
    quantity: int
    price: float