from fastapi import FastAPI
from src.contacts.routers import router as router_users
from src.auth.routers import router as router_users_app
app = FastAPI()

app.include_router(router_users, prefix="/users", tags=["users"])
app.include_router(router_users_app, prefix="/users_app", tags=["users_app"])