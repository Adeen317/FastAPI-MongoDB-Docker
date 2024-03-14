from typing import Union
from fastapi import APIRouter,Request,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.note import Note
from config.db import conn
from schemas.note import noteEntity,notesEntity

note= APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            #"important": doc["important"],
        })
        #print(doc)
    return templates.TemplateResponse(
        name="index.html", context={"request": request, "newDocs": newDocs})

# POST Request Handler
@note.post("/")
async def create_item(note: Note):
    # Assuming your MongoDB collection is named "notes"
    collection = conn.notes.notes
    # Inserting the new item
    result = collection.insert_one({"title": note.title, "desc": note.desc})
    if result.inserted_id:
        return {"message": "Item created successfully", "item_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create item")

