from http.client import HTTPException
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError

from common.rest_interface import DefaultHandler, RestResponse
from telescope.db_models import LocationDB, TelescopeSpecificationsDB, TelescopeDB, RoomDB
from telescope.responses import PostTelescopeResponse
from telescope.rest_models import TelescopeRequest


class PostTelescopeHandler(DefaultHandler):
    def __init__(self, db, controller):
        self.db = db
        self.controller = controller

    async def run(self, request: TelescopeRequest) -> PostTelescopeResponse:
        try:
            self.location_id = uuid4()
            self.specification_id = uuid4()
            self.telescope_id = str(uuid4())

            self.add_location(request)
            self.add_specification(request)
            self.add_telescope(request)
            await self.create_room_for_telescope()

            self.db.commit()
            response = PostTelescopeResponse(
                telescope_id=self.telescope_id, publish_token=self.publisher_key
            )
            return response
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def add_location(self, request):
        location = LocationDB(
            id=self.location_id,
            city=request.location.city,
            country=request.location.country,
            latitude=request.location.latitude,
            longitude=request.location.longitude,
        )
        self.db.add(location)

    def add_specification(self, request):
        specs = TelescopeSpecificationsDB(
            id=self.specification_id,
            aperture=request.specifications.aperture,
            focal_length=request.specifications.focal_length,
            focal_ratio=request.specifications.focal_ratio,
            weight=request.specifications.weight,
            length=request.specifications.length,
            width=request.specifications.width,
            height=request.specifications.height,
            mount_type=request.specifications.mount_type,
            optical_design=request.specifications.optical_design,
        )
        self.db.add(specs)

    def add_telescope(self, request):
        new_telescope = TelescopeDB(
            id=self.telescope_id,
            telescope_name=request.telescope_name,
            telescope_type=request.telescope_type,
            price_per_minute=request.price_per_minute,
            owner=request.owner,
            status=request.status,
            location_id=self.location_id,
            specifications_id=self.specification_id,
        )
        self.db.add(new_telescope)

    async def create_room_for_telescope(self):
        room_info = await self.controller.create_room(self.telescope_id)
        room_id = room_info.name
        self.publisher_key = self.controller.create_publisher_token(self.telescope_id, room_id)
        room = RoomDB(
            telescope_id=self.telescope_id, publisher_key=self.publisher_key, room_id=room_id
        )
        self.db.add(room)
