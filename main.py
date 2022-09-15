from enum import Enum
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

# Create an enum class


class ModelName(str, Enum):
    alexnet = "alexnet"
    restnet = "restnet"
    lenet = "lenet"

# Create Pydantic's Model


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


# Create a new instance
app = FastAPI()

fake_items_db = [
    {"item_name": "foo"},
    {"item_name": "bar"},
    {"item_name": "baz"}
]


@app.get('/')
async def root():
    return {"message": "Hello, world!"}

# Query parameters


@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# Order matters


@app.get('/users/me')
async def read_user_me():
    return {"user_id": "the current user"}


@app.get('/users/{user_id}')
async def read_user(user_id: int):
    return {"user_id": user_id}


# Predefind values with enum class


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# Data conversion and validation
# needy is a query parameter required


@app.get('/items/{item_id}')
async def read_items(
    item_id: str,
    needy: str,
    skip: int = 0,
    limit: Union[int, None] = None,
    q: Union[str, None] = None,
    short: bool = False
):
    item = {
        "item_id": item_id,
        "needy": needy,
        "skip": skip,
        "limit": limit
    }

    if q:
        item.update({q: q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item

# Multiple path and query parameters


@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item(
    user_id: int,
    item_id: str,
    q: Union[str, None] = None,
    short: bool = False
):
    item = {
        "item_id": item_id,
        "owner": user_id
    }

    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item


@app.post('/items/')
async def create_item(item: Item):
    return item
