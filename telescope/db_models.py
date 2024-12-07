from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy import Column, String, Float, Integer, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from telescope.rest_models import MountType, OpticalDesign, TelescopeType, TelescopeStatus

Base = declarative_base()

class LocationDB(Base):
    __tablename__ = "locations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String(100), default="Warsaw")
    country = Column(String(10), default="PL")
    latitude = Column(Float, default=55.5)
    longitude = Column(Float, default=55.5)

class TelescopeSpecificationsDB(Base):
    __tablename__ = "telescopespecifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aperture = Column(Float, nullable=False)
    focal_length = Column(Float, nullable=False)
    focal_ratio = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    mount_type = Column(Enum(MountType), nullable=False)
    optical_design = Column(Enum(OpticalDesign), nullable=False)

class TelescopeDB(Base):
    __tablename__ = "telescopes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name = Column(String(100))
    telescope_type = Column(Enum(TelescopeType), nullable=False)
    price_per_minute = Column(Float, nullable=False)
    owner = Column(String(100), nullable=False)
    status = Column(Enum(TelescopeStatus), nullable=False, default=TelescopeStatus.FREE)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    specifications_id = Column(UUID(as_uuid=True), ForeignKey("telescopespecifications.id"), nullable=False)

    location = relationship("LocationDB")
    specifications = relationship("TelescopeSpecificationsDB")

class TelescopeStateDB(Base):
    __tablename__ = "telescopestates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    telescope_id = Column(UUID(as_uuid=True), ForeignKey("telescopes.id"), nullable=False)
    action_time = Column(TIMESTAMP, default=datetime.utcnow)
    action_type = Column(String(50), nullable=False)