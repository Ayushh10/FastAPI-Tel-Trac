from random import randint
from fastapi import FastAPI
from model import Product

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Initiated"}

products = [
    Product(id=randint(1,100), name="iPhone", desc= "premium phone", price= 999, quantity= 100),
    Product(id=randint(1,100), name="Phone", desc= " phone", price= 999, quantity= 100),
    Product(id=randint(1,100), name="Machine", desc= "thing", price= 999, quantity= 100),
    Product(id=randint(1,100), name="Laptop", desc= "something", price= 999, quantity= 100),
    Product(id=randint(1,100), name="WashingMachine", desc= "premium phone", price= 999, quantity= 100)
]
@app.get("/product")
def get_prods():
    return products

@app.get("/product/search_id")
def search_prod(id: int):
    for prod in products:
        if prod.id == id:
            return prod
    return "Record Not Found"

@app.post("/product")
def add_prod(product: Product):
    products.append(product)
    return products

@app.put("/product")
def update_prod(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return {f"Product {id} updated": product}
    return "Product not found" 

@app.delete("/product")
def delete_prod(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Item removed"
    return "Item not found"