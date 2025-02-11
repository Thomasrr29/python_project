from sqlmodel import SQLModel, create_engine, Session 
from typing import Annotated
from fastapi import Depends 

DATABASE_URL = "postgresql+psycopg2://default:ObkhogH71VUe@ep-royal-recipe-a45z89em-pooler.us-east-1.aws.neon.tech/verceldb?sslmode=require"

engine = create_engine(DATABASE_URL, echo=True)

def get_session(): 

    with Session(engine) as session: 
        yield session 

def create_tables(): 

    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]


