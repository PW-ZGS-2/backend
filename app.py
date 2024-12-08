import os

from fastapi import FastAPI, Depends
from fastapi_utilities import repeat_every
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.middleware.cors import CORSMiddleware

from pricing.pricing_route import pricing_router
from telescope.db_models import RoomDB
from telescope.handler import DeleteTelescopeHandler
from telescope.livekit_controller import LiveKitController
from telescope.telescope_route import telescope_router, SessionLocal

app = FastAPI(
    title="SkyShare",
    description="SkyShareAPI",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


app.include_router(telescope_router, tags=["Telescope"])
app.include_router(pricing_router, tags= ["Pricing"])



import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
