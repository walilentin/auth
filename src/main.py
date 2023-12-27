from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

import uvicorn
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.auth.router import router as auth_router
from src.users.router import router as user_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=auth_router, prefix=settings.api_v1_prefix)
app.include_router(router=user_router, prefix=settings.api_v1_prefix)

@app.get("/")
async def hello_index():
    return {
        "message": "Hello index!",
    }
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)