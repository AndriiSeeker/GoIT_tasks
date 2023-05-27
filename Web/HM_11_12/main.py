import os

import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from src.database.db import get_db
from src.routes import contacts, auth, users
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(swagger_ui_parameters={"operationsSorter": "method"})

templates = Jinja2Templates(directory='src/templates')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT')),
                          password=os.environ.get('REDIS_PASSWORD'), db=0, encoding="utf-8")
    await FastAPILimiter.init(r)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={"request": request})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to my Rest API example"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')
