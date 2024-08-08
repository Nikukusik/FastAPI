import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.contacts.routers import router as router_users
from src.auth.routers import router as router_users_app
import os
from fastapi_limiter import FastAPILimiter
from config.general import REDIS_PORT, REDIS_HOST

origins = [
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

app.include_router(router_users, prefix="/users", tags=["users"])
app.include_router(router_users_app, prefix="/users_app", tags=["users_app"])