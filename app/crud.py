from sqlmodel import Session, select
from .models import Note, engine

# open database session
def create_note(note: Note):
    with Session(engine) as session:
        session.add(note) # add note to DB
        session.commit() # commit change
        session.refresh(note) # refresh object to get the id from DB
        return note # return full saved object
    
# returns all notes as a list by running SELECT * FROM note
def get_notes():
    with Session(engine) as session:
        return session.exec(select(Note)).all()
    
# find and return note using primary key id
def get_note(note_id: int):
    with Session(engine) as session:
        return session.get(Note, note_id)
    
# function to update an existing note in the db
def update_note(note_id: int, data: dict):
    with Session(engine) as session:
        note = session.get(Note, note_id)  # retrieves specific note by id
        if not note:    # if note id does not exist, return None
            return None
        for key, value in data.items(): # update object with new data and save
            setattr(note, key, value)
        session.add(note)
        session.commit()
        session.refresh(note)
        return note

# delete an existing note in the database by id
def delete_note(note_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:    # if note id doesn't exist, return None
            return None
        session.delete(note) # delete note and commit change
        session.commit()
        return True