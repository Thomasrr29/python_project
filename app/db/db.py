from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from fastapi import Depends 

DATABASE_URL = "postgresql+asyncpg://default:ObkhogH71VUe@ep-royal-recipe-a45z89em-pooler.us-east-1.aws.neon.tech/verceldb"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]: 

    async with async_session_maker() as session: 
        yield session 

async def create_tables(): 

    async with engine.begin() as coon: 
    
        await coon.run_sync(SQLModel.metadata.create_all)