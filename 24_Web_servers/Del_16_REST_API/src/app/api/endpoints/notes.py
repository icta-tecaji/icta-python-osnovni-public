from typing import List

from app.crud import notes
from app.schemas.notes import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await notes.get_all()


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int):
    note = await notes.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await notes.post(payload)
    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.put("/{id}/", response_model=NoteDB)
async def update_note(id: int, payload: NoteSchema):
    note = await notes.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await notes.put(id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int):
    note = await notes.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await notes.delete(id)
    return note
