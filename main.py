from beanie import init_beanie
from fastapi import FastAPI
from connection.connection import ping_server, db
from models.movie_model import Movie
from models.user_model import User
from routes.movie_route import router_movie
from routes.user_route import router_user
from routes.auth_route import router_auth
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ping_server()
    # Inicializa Beanie
    await init_beanie(database=db, document_models=[Movie, User])
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router_movie)
app.include_router(router_user)
app.include_router(router_auth)
