from fastapi import FastAPI
from threading import Thread
import uvicorn
import router

app = FastAPI()
app.include_router(router.router)

