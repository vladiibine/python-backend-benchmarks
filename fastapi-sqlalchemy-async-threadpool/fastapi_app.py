import asyncio
import contextvars
import functools
import os
import typing

from fastapi import FastAPI
from fastapi import status, HTTPException

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy import select


DB_DATABASE = os.environ['POSTGRES_DB']
DB_USER = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_HOST = os.environ['POSTGRES_HOST']
DB_PORT = os.environ.get('POSTGRES_PORT', '5432')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

T = typing.TypeVar("T")

metadata = sqlalchemy.MetaData()

Base = declarative_base()


class Permission(Base):
    __tablename__ = "auth_permission"
    id = Column(Integer, primary_key=True)


engine = create_engine(
        DATABASE_URL,
        # echo=True,
    )

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI(name="App", description="blabla")


# @app.on_event("startup")
# async def startup():
#     await engine.connect()


@app.on_event("shutdown")
async def shutdown():
    await engine.disconnect()


async def run_in_threadpool(
    func: typing.Callable[..., T], *args: typing.Any, **kwargs: typing.Any
) -> T:
    loop = asyncio.get_event_loop()
    if contextvars is not None:  # pragma: no cover
        # Ensure we run in the same context
        child = functools.partial(func, *args, **kwargs)
        context = contextvars.copy_context()
        func = context.run
        args = (child,)
    elif kwargs:  # pragma: no cover
        # loop.run_in_executor doesn't accept 'kwargs', so bind them in here
        func = functools.partial(func, **kwargs)
    return await loop.run_in_executor(None, func, *args)


@app.get('/0q/')
async def handler():
    return "Hello world"


@app.get("/1q/", status_code=status.HTTP_200_OK)
async def handler1():
    with SyncSessionLocal() as session:
        result = await run_in_threadpool(
            lambda: session.execute(select(func.count('*')).select_from(Permission))
        )

    return list(result)[0][0]


@app.get("/10q/", status_code=status.HTTP_200_OK)
async def handler2():
    with SyncSessionLocal() as session:
        # async with session.begin():
        counter = 0
        for _ in range(10):
            result = await run_in_threadpool(
                lambda: session.execute(select(func.count('*')).select_from(Permission))
            )

            counter += list(result)[0][0]

    return str(counter)
