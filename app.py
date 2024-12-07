from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from telescope.telescope_route import telescope_router

app = FastAPI(
    title="Telescope",
    description="TelescopeAPI",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

app.include_router(telescope_router, tags=["Telescope"])

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)