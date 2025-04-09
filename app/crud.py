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
def get_notes_for_user(user_id: int):
    with Session(engine) as session:
        return session.exec(select(Note).where(Note.ownder_id == user_id)).all()
    
# find and return note using primary key id
def get_note_by_id_for_user(note_id: int, user_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if note and note.owner_id == user_id:
            return note
        return None
    
# function to update an existing note in the db
def update_note(note_id: int, data: dict, user_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)  # retrieves specific note by id
        if not note or note.owner_id != user_id:    # if note id does not exist or does not belong to the user, return none
            return None
        for key, value in data.items(): # update object with new data and save
            setattr(note, key, value)
        session.add(note)
        session.commit()
        session.refresh(note)
        return note

# delete an existing note in the database by id
def delete_note(note_id: int, user_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note or note.owner_id != user_id:    # if note id doesn't exist or does not belong, return none
            return None
        session.delete(note) # delete note and commit change
        session.commit()
        return True