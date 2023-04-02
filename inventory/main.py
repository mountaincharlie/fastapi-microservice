import os
from environs import Env

from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel

env = Env()
env.read_env()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()

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
    quantity_available: int

    class Meta:
        database = redis


@app.get("/products")
def all_products():
    """
    Get all products from the redis db
    """
    return []
