from fastapi import FastAPI
from threading import Thread
import uvicorn
import app.api.dependencies as router
import app.dependencies.check as check

app = FastAPI()
app.include_router(router.router)

def check():
    t1 = Thread(target=uvicorn.run, args=(app,))
    # TODO: ADD UI THREAD
