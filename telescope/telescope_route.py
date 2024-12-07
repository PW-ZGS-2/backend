from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

from rest_models import Telescope, TelescopeSpecifications, MountType, OpticalDesign, Location
from telescope.responses import TelescopeIdResponse, TelescopesResponse, RegisteredTelescope, TelescopeStateResponse
from telescope.rest_models import TelescopeStatus

telescope_router = APIRouter(prefix="/telescopes")

# @telescope_router.get("/")
# async def get_telescope(owner: Owner):
#     return "hi"

@telescope_router.post("/", response_model=TelescopeIdResponse)
async def post_telescope(telescope: Telescope):
    id = str(uuid.uuid4())
    return TelescopeIdResponse(telescope_id=id)

@telescope_router.patch("/{telescope_id}", response_model=TelescopeIdResponse)
async def patch_telescope(telescope_id: str,telescope: Telescope):
    return TelescopeIdResponse(telescope_id=telescope_id)

@telescope_router.get("/list", response_model=TelescopesResponse)
async def get_telescopes_list():
    return TelescopesResponse(available_telescopes=1,reserved_telescopes=1,unavailable_telescopes=1,
                              telescopes = [RegisteredTelescope(model_name = "model_1",price_per_day =20.2,
                                                                location={"city": "warsaw","country": 'Pl',"latitude": 55,"longitude": 55},
                                                                status = "AVAILABLE")])
@telescope_router.get("/{telescope_id}", response_model=TelescopeSpecifications)
async def get_telescope_details(telescope_id: str):
    return TelescopeSpecifications(aperture=0.0,
focal_length=0.0,
focal_ratio=0.0,
weight=0.0,
length=0.0,
width=0.0,
height=0.0,mount_type=MountType.GO_TO,
optical_design=OpticalDesign.REFLECTOR,)

@telescope_router.post("/{telescope_id}/{state}")
async def lock_telescope(telescope_id: str, state: TelescopeStatus):
    return TelescopeStateResponse(telescope_id=telescope_id, state=state)

# @telescope_router.get("/telescopes/", response_model=List[Telescope])
# async def list_telescopes():
#     return "hi"
#
# @telescope_router.get("/telescope/{telescope_id}", response_model=Telescope)
# async def get_telescope(telescope_id: int):
#     return "hi"
#
# @telescope_router.post("/reserve/", response_model=Reservation)
# async def reserve_telescope(reservation: Reservation):
#     # Check if the telescope exists
#     return "hi"