from fastapi import FastAPI, HTTPException, Depends
from app.models import Note, create_db_and_tables, engine, User
from app.crud import create_note, get_notes_for_user, get_note_by_id_for_user, update_note, delete_note
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth import hash_password, verify_password, create_access_token, decode_access_token
from sqlmodel import select, Session
from contextlib import asynccontextmanager


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# startup logic
@asynccontextmanager
async def lifespan(app: FastAPI):
     create_db_and_tables()
     yield

app = FastAPI(lifespan=lifespan)

# this function is used to protect endpoints by reading the token, decoding to get username, loads only that user, and returns the user object for the route
def get_current_user(token: str = Depends(oauth2_scheme)):
     username = decode_access_token(token)
     if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
     with Session(engine) as session:
          user = session.exec(select(User).where(User.username == username)).first()
          if not user:
               raise HTTPException(status_code=401, details="User not found")
          return user

# accepts new unique usernames and passwords to create new users and add them to the database
@app.post("/signup")
def signup(form_data: OAuth2PasswordRequestForm = Depends()):
     with Session(engine) as session:
          existing_user = session.exec(select(User).where(User.username == form_data.username)).first()
          if existing_user:
               raise HTTPException(status_code=400, detail="Username already exists")
          user = User(username=form_data.username, password_hash=hash_password(form_data.password))
          session.add(user)
          session.commit()
          session.refresh(user)
          return{"msg": "User created"}
     
# verifies user credentials and returns a JWT token is successful
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
     with Session(engine) as session:
          user = session.exec(select(User).where(User.username == form_data.username)).first()
          if not user or not verify_password(form_data.password, user.password_hash):
               raise HTTPException(status_code=401, detail="Invalid credentials")
          token = create_access_token({"sub": user.username})
          return {"access_token": token, "token_type": "bearer"}

# accepts a new note (validated by FastAPI), then creates and returns the saved note
@app.post("/notes/", response_model=Note)
def add_note(note: Note, user: User = Depends(get_current_user)):
    note.owner_id = user.id
    return create_note(note)

# returns all notes
@app.get("/notes/", response_model=list[Note])
def read_notes(user: User = Depends(get_current_user)):
    return get_notes_for_user(user.id)

# returns a specific note by id if found, otherwise otherwise returns a 404 error
@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, user: User = Depends(get_current_user)):
    note = get_note_by_id_for_user(note_id)
    if not Note or note.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# updates an existing note using key-value pairs
@app.put("/notes/{note_id}", response_model=Note)
def edit_note(note_id: int, data:dict, user: User = Depends(get_current_user)):
    updated = update_note(note_id, data, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found or not yours")
    return updated

# deletes a note found by id and returns a confirmation
@app.delete("/notes/{note_id}")
def remove_note(note_id: int, user: User = Depends(get_current_user)):
    deleted = delete_note(note_id, user.id)
    if not deleted:
            raise HTTPException(status_code=404, detail="Note not found")
    return {"deleted": True}