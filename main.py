from fastapi import FastAPI

from utils.bootstrap import init_db
from utils.bootstrap import init_ai

app = FastAPI()

init_db()
init_ai()

from api.routers import chatbot, qa

app.include_router(chatbot.router)
app.include_router(qa.router)

