from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship
from typing import Optional, List

# create a User class and table with credentials and ownership to maintain security and exclusivity for data
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    notes: List["None"] = Relationship(back_populates="ownder")

# create table Note with 5 columns id(optional but primary key), title, content, owner_id, and owner
class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="notes")

sqlite_url = "sqlite:///./notes.db" # connects to a local SQLite DB file named notes.db
engine = create_engine(sqlite_url, echo=True) # create the engine and echo = True will log all SQL commands to the terminal for debugging purposes

# create database table if it doesn't already exist
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)