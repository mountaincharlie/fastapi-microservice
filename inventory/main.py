import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

if os.path.isfile('env.py'):
    import env
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

app = FastAPI()

# to allow cross origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

# creating a redis connection
redis = get_redis_connection(
    host=DB_HOST,
    port=DB_PORT,
    password=DB_PASSWORD,
    decode_responses=True
)


class Product(HashModel):
    """
    Creating a product model inheriting form HashModel
    Connected to the redis db
    """
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


# ---- CRUD functionality for products

def format(pk: str):
    """
    Takes pk as a string and formats the output for getting
    a product
    """
    product = Product.get(pk)
    return {
        "id": pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


@app.get("/products")
def all():
    """
    Get all products from the redis db
    Returns a list of all products formatted with format() 
    """
    return [format(pk) for pk in Product.all_pks()]


@app.post("/products")
def create(product: Product):
    """
    Creates a product
    Uses post method to products endpoint
    Takes in product (according to the Product model) and returns product.save()
    """
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    """
    Gets the product by pk
    """
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    """
    Deletes a product of particular pk
    """
    return Product.delete(pk)
