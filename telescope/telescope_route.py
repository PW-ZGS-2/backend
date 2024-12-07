from fastapi import APIRouter
import uuid

from telescope.rest_models import Telescope, TelescopeSpecifications, MountType, OpticalDesign, Location
from telescope.responses import TelescopeIdResponse, TelescopesResponse, RegisteredTelescope, TelescopeStateResponse
from telescope.rest_models import TelescopeStatus

telescope_router = APIRouter(prefix="/telescopes")


@telescope_router.post("/", response_model=TelescopeIdResponse)
async def post_telescope(telescope: Telescope):
    id = str(uuid.uuid4())
    return TelescopeIdResponse(telescope_id=id)

@telescope_router.patch("/{telescope_id}", response_model=TelescopeIdResponse)
async def patch_telescope(telescope_id: str,telescope: Telescope):
    return TelescopeIdResponse(telescope_id=telescope_id)

@telescope_router.get("/list", response_model=TelescopesResponse)
async def get_telescopes_list():
    return TelescopesResponse(available_telescopes=2,reserved_telescopes=1,unavailable_telescopes=0,
                              telescopes = [RegisteredTelescope(model_name = "model_1",price_per_day =20.2,
                                                                location={
                "city": "Łódź",
                "country": "Poland",
                "latitude": 51.7592,
                "longitude": 19.4559
            },
                                                                status = "FREE"),RegisteredTelescope(model_name = "model_1",price_per_day =20.2,
                                                                location= {
                "city": "Bydgoszcz",
                "country": "Poland",
                "latitude": 53.1235,
                "longitude": 18.0084
            },
                                                                status = "LOCK"),
                                            RegisteredTelescope(model_name="model_1", price_per_day=20.2,
                                                                location= {
                "city": "Gdańsk",
                "country": "Poland",
                "latitude": 54.3520,
                "longitude": 18.6466
            },
                                                                status="FREE")
                                            ])
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

