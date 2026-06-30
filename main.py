from random import randint
from fastapi import Depends, FastAPI
from model import Product
from database import engine, session
import db_model
from sqlalchemy.orm import Session


app = FastAPI()

db_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API Initiated"}

products = [
    Product(id=randint(1,100), name="iPhone", describe= "premium phone", price= 999, quantity= 100),
    Product(id=randint(1,100), name="Phone", describe= " phone", price= 999, quantity= 100),
    Product(id=randint(1,100), name="Machine", describe= "thing", price= 999, quantity= 100),
    Product(id=randint(1,100), name="Laptop", describe= "something", price= 999, quantity= 100),
    Product(id=randint(1,100), name="WashingMachine", describe= "premium phone", price= 999, quantity= 100)
]

def get_db():
    db = session()
    try: 
        yield db
    finally:
        db.close()

@app.get("/product")
def init_db(db: Session = Depends(get_db)):
    # db = session()
    count = db.query(db_model.Product).count
    if count == 0:
        for prod in products:
            db.add(db_model.Product(**prod.model_dump()))
        db.commit()

init_db()

@app.get("/products")
def get_prods(db: Session = Depends(get_db)):
    db_products = db.query(db_model.Product).all()
    return db_products

@app.get("/product/search")
def search_by_id(id: int, db : Session = Depends(get_db)):
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not Found"


@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(db_model.Product(**product.model_dump()))
    db.commit()

@app.put("/product")
def update_product(id: int, product : Product, db : Session = Depends(get_db)):
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.describe = product.describe
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Record updated"
    return "Record Not Found"

@app.delete("/product")
def delete_product(id: int, db : Session = Depends(get_db)):
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    return "Product not Found"

# @app.get("/product/search_id")
# def search_prod(id: int):
#     for prod in products:
#         if prod.id == id:
#             return prod
#     return "Record Not Found"

# @app.post("/product")
# def add_prod(product: Product):
#     products.append(product)
#     return products

# @app.put("/product")
# def update_prod(id: int, product: Product):
#     for i in range(len(products)):
#         if products[i].id == id:
#             products[i] = product
#             return {f"Product {id} updated": product}
#     return "Product not found" 
# 
# @app.delete("/product")
# def delete_prod(id: int):
#     for i in range(len(products)):
#         if products[i].id == id:
#             del products[i]
#             return "Item removed"
#     return "Item not found"