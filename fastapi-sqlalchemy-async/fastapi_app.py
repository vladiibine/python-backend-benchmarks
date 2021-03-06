import os

from fastapi import FastAPI
from fastapi import status, HTTPException

from pydantic import BaseModel

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy import select


DB_DATABASE = os.environ['POSTGRES_DB']
DB_USER = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_HOST = os.environ['POSTGRES_HOST']
DB_PORT = os.environ.get('POSTGRES_PORT', '5432')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# db = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

Base = declarative_base()


class Permission(Base):
    __tablename__ = "auth_permission"
    id = Column(Integer, primary_key=True)


engine = create_async_engine(
        DATABASE_URL,
        # echo=True,
    )

AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


class ApiCompany(BaseModel):
    vat: str
    description: str


app = FastAPI(name="app", description="blabla")


# @app.on_event("startup")
# async def startup():
#     await engine.connect()


@app.on_event("shutdown")
async def shutdown():
    await engine.disconnect()


@app.get('/0q/')
async def handler():
    return "Hello world"


@app.get("/1q/", status_code=status.HTTP_200_OK)
async def handler1():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count('*')).select_from(Permission))

    return list(result)[0][0]


@app.get("/10q/", status_code=status.HTTP_200_OK)
async def handler2():
    async with AsyncSessionLocal() as session:
        # async with session.begin():
        counter = 0
        for _ in range(10):
            result = await session.execute(select(func.count('*')).select_from(Permission))

            counter += list(result)[0][0]

    return str(counter)
