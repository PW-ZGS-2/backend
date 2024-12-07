from uuid import UUID

from pydantic import BaseModel, ConfigDict

from telescope.rest_models import Location, TelescopeStatus


class TelescopeIdResponse(BaseModel):
    model_config = ConfigDict(json_encoders={UUID: str})

    telescope_id: str


class TelescopeStateResponse(BaseModel):
    telescope_id: str
    state: TelescopeStatus

    class Config:
        use_enum_values = True

class RegisteredTelescope(BaseModel):
    telescope_id: str
    model_name: str
    price_per_day: float
    location: Location
    status: TelescopeStatus


class TelescopesResponse(BaseModel):
    available_telescopes: int
    reserved_telescopes: int
    unavailable_telescopes: int
    telescopes: list[RegisteredTelescope]

