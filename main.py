import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Retrieve DB Connection string from environment variable
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["my_app_db"]
items_collection = db["items"]

class Item(BaseModel):
    name: str
    description: str

@app.get("/")
def read_root():
    return {"status": "Backend running successfully"}

@app.post("/items")
def create_item(item: Item):
    result = items_collection.insert_one(item.dict())
    return {"id": str(result.inserted_id), "message": "Item created"}

@app.get("/items")
def get_items():
    items = list(items_collection.find({}, {"_id": 0}))
    return {"data": items}