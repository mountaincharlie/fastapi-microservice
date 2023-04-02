import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests

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

# the Payments microservice should have a different database (but in this case redis is only free for 1)
redis = get_redis_connection(
    host=DB_HOST,
    port=DB_PORT,
    password=DB_PASSWORD,
    decode_responses=True
)


class Order(HashModel):
    """
    db model for Orders, inheriting HashModel
    """
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        """
        Connecting to the redis db
        """
        database = redis


# ---- CRUD functionality for orders

@app.post("/orders")
async def create(request: Request):
    """
    Creating an order to be added to the redis db
    Using async functinoality to await the request
    """
    body = await request.json()

    # sending a request to the Inventory microservice (getting the url for a product by pk string)
    req = requests.get(f"http://127.0.0.1:8000/products/{str(body['id'])}")
    product = req.json()

    # creating the Order
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=round(product['price']*0.2, 2),
        total=round(product['price']*1.2, 2),
        quantity=body['quantity'],
        status="pending"
    )
    order.save()

    order_completed(order)

    return order


def order_completed(order: Order):
    """
    MORE COMPLICATED FUNCTINOALITY COMING
    Sets order status to 'completed'
    """
    time.sleep(5)  # allows 5 seconds for the payment processor to run
    order.status = 'completed'
    order.save()
