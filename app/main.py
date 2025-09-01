from fastapi import FastAPI
from .routers.statusRouter import statusRouter
from .routers.agentRouter import agentRouter
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(statusRouter)

app.include_router(agentRouter)
