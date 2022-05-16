from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import login, utilisateur 


origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"]
)
app.include_router(login.router)
app.include_router(utilisateur.router)

@app.get("/")
def root():
    return {"message": "Hello world, by a backend programmer"}

#@app.on_event("startup")
#async def create_db():
#    await get_db()