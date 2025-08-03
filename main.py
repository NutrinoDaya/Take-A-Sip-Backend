# app/main.py
import logging
import uvicorn
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes import auth, food
from db.database import client, create_indexes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    await create_indexes()
    yield
    # On shutdown
    client.close()
    logging.info("MongoDB connection closed.")


app = FastAPI(title="Caffe App API", lifespan=lifespan)

# Include routers from the api directory
app.include_router(auth.router)
app.include_router(food.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Caffe App API!"}

# This block allows you to run the server directly from this file
if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)