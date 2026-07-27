import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Enable CORS for Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from Flutter Web running on localhost
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

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