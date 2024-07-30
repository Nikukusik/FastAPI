from fastapi import FastAPI, Depends
from routers import router as router_users
app = FastAPI()

app.include_router(router_users, prefix="/users", tags=["users"])