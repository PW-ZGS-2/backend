from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TelescopeType(str, Enum):
    MOCK = "MOCK"
    OPEN_SOURCE = "OPEN_SOURCE"
    PROFESSIONAL = "PROFESSIONAL"


class TelescopeStatus(str, Enum):
    FREE = "FREE"
    LOCK = "LOCK"
    DAMAGED = "DAMAGED"


class Location(BaseModel):
    city: str | None = "warsaw"
    country: str | None = "pl"
    latitude: float = 55.5
    longitude: float = 55.5


class User(BaseModel):
    first_name: str
    second_name: str
    phone: str | None
    address: str | None


class MountType(str, Enum):
    ALT_AZ = "ALT_AZ"  # Altitude-Azimuth mount
    EQ = "EQUATORIAL"  # Equatorial mount
    DOB = "DOBSONIAN"  # Dobsonian mount
    GO_TO = "GOTO"  # Motorized, computer-controlled mount


# Enum for Optical Design Type
class OpticalDesign(str, Enum):
    REFLECTOR = "Reflector"
    REFRACTOR = "Refractor"
    CATADIOPTRIC = "Catadioptric"
    SCHMIDT = "Schmidt-Cassegrain"
    MAK = "Maksutov"
    COMBINATION = "Combination"


class TelescopeSpecifications(BaseModel):
    aperture: float  # Diameter of the primary lens or mirror in cm
    focal_length: float  # Focal length in mm
    focal_ratio: float  # Focal ratio (f/number)
    weight: float  # Weight in kg
    length: float  # Length of the telescope tube in cm
    width: float  # Width of the telescope tube in cm
    height: float  # Height of the telescope in cm
    mount_type: MountType  # Type of mount (e.g., Alt-Az, Equatorial, Dobsonian)
    optical_design: OpticalDesign


class TelescopeRequest(BaseModel):
    telescope_name: str = "Model 1"
    telescope_type: TelescopeType = TelescopeType.OPEN_SOURCE
    price_per_minute: float = "20"
    owner: str = "Damianek"
    location: Location
    status: TelescopeStatus = TelescopeStatus.FREE
    specifications: TelescopeSpecifications

    class Config:
        use_enum_values = True
        json_schema_exclude = {"id"}


class TelescopeState(BaseModel):
    user_name: str
    telescope_id: int
    action_time: datetime
    action_type: datetime
