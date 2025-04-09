from fastapi import FastAPI, HTTPException
from app.models import Note, create_db_and_tables
from app.crud import create_note, get_notes, get_note, update_note, delete_note

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()  # runs once when app starts to make sure tables exist

# accepts a new note (validated by FastAPI), then creates and returns the saved note
@app.post("/notes/", response_model=Note)
def add_note(note: Note):
    return create_note(note)

# returns all notes
@app.get("/notes/", response_model=list[Note])
def read_notes():
    return get_notes()

# returns a specific note by id if found, otherwise otherwise returns a 404 error
@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int):
    note = get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# updates an existing note using key-value pairs
@app.put("/notes/{note_id}", response_model=Note)
def edit_note(note_id: int, data:dict):
    updated = update_note(note_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

# deletes a note found by id and returns a confirmation
@app.delete("/notes/{note_id}")
def remove_note(note_id: int):
    deleted = delete_note(note_id)
    if not deleted:
            raise HTTPException(status_code=404, detail="Note not found")
    return {"deleted": True}