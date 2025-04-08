from sqlmodel import Field, SQLModel, create_engine, Session, select

class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary=True)
    title: str
    content: str

sqlite_url = "sqlite:///./notes.db"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)