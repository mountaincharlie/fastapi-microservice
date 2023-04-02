import os
# from environs import Env

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

# print(os.environ)

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


@app.get("/products")
def all():
    """
    Get all products from the redis db
    """
    return Product.all_pks()
