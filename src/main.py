from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from src.core.config import settings
from src.demo_jwt_auth.demo_jwt_auth import router
from src.users.router import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router, prefix=settings.api_v1_prefix)
app.include_router(router=user_router)

@app.get("/")
async def hello_index():
    return {
        "message": "Hello index!",
    }


@app.get("/hello/")
async def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}


@app.get("/calc/add/")
async def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)