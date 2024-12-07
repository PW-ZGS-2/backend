import os
from typing import Generator
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from sqlalchemy.exc import SQLAlchemyError

from telescope.db_models import (
    TelescopeDB,
    LocationDB,
    TelescopeSpecificationsDB,
    TelescopeStateDB,
    RoomDB,
)
from telescope.handler import PostTelescopeHandler
from telescope.livekit_controller import LiveKitController
from telescope.rest_models import (
    TelescopeRequest,
    TelescopeSpecifications,
)
from telescope.responses import (
    TelescopesResponse,
    RegisteredTelescope,
    StateResponse,
    PostTelescopeResponse,
)
from telescope.rest_models import TelescopeStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session

telescope_router = APIRouter(prefix="/telescopes")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#
async def get_livekit_controller() -> Generator[LiveKitController, None, None]:
    controller = LiveKitController()
    yield controller
    await controller.close()
    del controller


@telescope_router.post("/", response_model=PostTelescopeResponse)
async def post_telescope(
    telescope: TelescopeRequest,
    db: Session = Depends(get_db),
    controller: LiveKitController = Depends(get_livekit_controller),
):
    handler = PostTelescopeHandler(db,controller)
    response = await handler.run(telescope)
    return response


@telescope_router.put("/{telescope_id}", response_model=PostTelescopeResponse)
async def patch_telescope(
    telescope_id: str, telescope: TelescopeRequest, db: Session = Depends(get_db)
):
    telescope_id = str(telescope_id)
    existing_telescope = (
        db.query(TelescopeDB).filter(TelescopeDB.id == telescope_id).first()
    )
    if not existing_telescope:
        raise HTTPException(status_code=404, detail="Telescope not found")
    db.delete(existing_telescope)
    db.commit()

    # Delete related objects
    db.query(TelescopeStateDB).filter(
        TelescopeStateDB.telescope_id == telescope_id
    ).delete()
    db.query(TelescopeSpecificationsDB).filter(
        TelescopeSpecificationsDB.id == existing_telescope.specifications_id
    ).delete()
    db.query(LocationDB).filter(
        LocationDB.id == existing_telescope.location_id
    ).delete()

    db.commit()
    location = LocationDB(
        city=telescope.location.city,
        country=telescope.location.country,
        latitude=telescope.location.latitude,
        longitude=telescope.location.longitude,
    )
    db.add(location)
    db.commit()
    db.refresh(location)

    # Create new telescope specifications
    specs = TelescopeSpecificationsDB(
        aperture=telescope.specifications.aperture,
        focal_length=telescope.specifications.focal_length,
        focal_ratio=telescope.specifications.focal_ratio,
        weight=telescope.specifications.weight,
        length=telescope.specifications.length,
        width=telescope.specifications.width,
        height=telescope.specifications.height,
        mount_type=telescope.specifications.mount_type,
        optical_design=telescope.specifications.optical_design,
    )
    db.add(specs)
    db.commit()
    db.refresh(specs)

    # Create the new telescope object
    new_telescope = TelescopeDB(
        id=telescope_id,  # Keep the same id
        telescope_name=telescope.telescope_name,
        telescope_type=telescope.telescope_type,
        price_per_minute=telescope.price_per_minute,
        owner=telescope.owner,
        status=telescope.status,
        location_id=str(location.id),
        specifications_id=str(specs.id),
    )

    db.add(new_telescope)
    db.commit()
    db.refresh(new_telescope)

    return PostTelescopeResponse(
        telescope_id=str(new_telescope.id), publish_token="231312"
    )


@telescope_router.delete("/{telescope_id}")
async def delete_telescope(telescope_id: str, db: Session = Depends(get_db)):
    telescope_id = str(telescope_id)

    existing_telescope = (
        db.query(TelescopeDB).filter(TelescopeDB.id == telescope_id).first()
    )

    if not existing_telescope:
        raise HTTPException(status_code=404, detail="Telescope not found")

    db.delete(existing_telescope)

    db.query(TelescopeStateDB).filter(
        TelescopeStateDB.telescope_id == telescope_id
    ).delete()

    db.query(TelescopeSpecificationsDB).filter(
        TelescopeSpecificationsDB.id == existing_telescope.specifications_id
    ).delete()

    db.query(LocationDB).filter(
        LocationDB.id == existing_telescope.location_id
    ).delete()

    db.commit()

    # Step 6: Return the ID of the deleted telescope
    return PostTelescopeResponse(telescope_id=telescope_id)


@telescope_router.get("/list", response_model=TelescopesResponse)
async def get_telescopes_list(db: Session = Depends(get_db)):
    available_telescopes = (
        db.query(TelescopeDB).filter(TelescopeDB.status == TelescopeStatus.FREE).count()
    )
    reserved_telescopes = (
        db.query(TelescopeDB).filter(TelescopeDB.status == TelescopeStatus.LOCK).count()
    )
    unavailable_telescopes = (
        db.query(TelescopeDB)
        .filter(TelescopeDB.status == TelescopeStatus.DAMAGED)
        .count()
    )

    telescopes = db.query(TelescopeDB).all()  # Or filter based on your criteria

    return TelescopesResponse(
        available_telescopes=available_telescopes,
        reserved_telescopes=reserved_telescopes,
        unavailable_telescopes=unavailable_telescopes,
        telescopes=[
            RegisteredTelescope(
                telescope_id=str(t.id),
                telescope_name=t.telescope_name,
                price_per_day=t.price_per_minute,
                location={
                    "city": t.location.city,
                    "country": t.location.country,
                    "latitude": t.location.latitude,
                    "longitude": t.location.longitude,
                },
                status=t.status.name,
            )
            for t in telescopes
        ],
    )


@telescope_router.get("/{telescope_id}", response_model=TelescopeSpecifications)
async def get_telescope_details(telescope_id: str, db: Session = Depends(get_db)):
    telescope = db.query(TelescopeDB).filter(TelescopeDB.id == telescope_id).first()
    if not telescope:
        raise HTTPException(status_code=404, detail="Telescope not found")

    specs = (
        db.query(TelescopeSpecificationsDB)
        .filter(TelescopeSpecificationsDB.id == telescope.specifications_id)
        .first()
    )
    return specs


@telescope_router.post(
    "/{user_id}/{telescope_id}/{state}", response_model=StateResponse
)
async def lock_telescope(
    user_id: str,
    telescope_id: str,
    state: TelescopeStatus,
    controller: LiveKitController = Depends(get_livekit_controller),
    db: Session = Depends(get_db),
):
    room = db.query(RoomDB).filter(RoomDB.telescope_id == telescope_id).first()
    sub_token = controller.create_subscriber_token(
        user_id, telescope_id, str(room.room_id)
    )

    return StateResponse(subscribe_token=sub_token)
