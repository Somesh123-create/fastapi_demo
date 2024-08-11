from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items", description="This is List all items")
async def list_items(skip: int=0, limit: int=10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def put_item(item_id: int, item:Item):
    return {"item_name": item.name, "item_id":item_id}

@app.get("/items_filter/{items_id}")
async def get_item(item_id: int, q: str | None =None):
    if q:
        return {"items_id": item_id, "q": q}
    return {"item_id":item_id}


@app.get("/items_list/extra_filter")
async def filter_data(item_id: int, sample_query: str, q: str | None = None, short: bool = False):
    items = {"item_id": item_id, "sample_query":sample_query}
    if q:
        items.update({"query": q})
    if not short:
        items.update({
            "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse id."
        })
    return items


class Items(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None



@app.post("/items/")
async def create_item(item:Items):
    return item


@app.put("/item_extra/{item_id}")
async def create_item_with_put(item_id: int, item:Items, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q":q})
    return result
