from sqlmodel import Field, SQLModel, create_engine, Session, select

# create table Note with 3 columns id(optional but primary key), title, and content
class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary=True)
    title: str
    content: str

sqlite_url = "sqlite:///./notes.db" # connects to a local SQLite DB file named notes.db
engine = create_engine(sqlite_url, echo=True) # create the engine and echo = True will log all SQL commands to the terminal for debugging purposes

# create database table if it doesn't already exist
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)