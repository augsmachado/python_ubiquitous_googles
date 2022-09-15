from typing import Union

from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Declare a variable as a str
# and get editor support inside the function


def main(user_id: str):
    return user_id

# A Pydantic User model


class User(BaseModel):
    id: int
    name: str
    joined: date

# A Pydantic Item model


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "world"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
