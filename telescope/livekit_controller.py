from livekit import api
from typing import Generator


class LiveKitController:
    def __init__(self, url="http://localhost:7880", api_key="devkey", api_secret="secret"):
        self.lkapi = api.LiveKitAPI(
            url="http://localhost:7880",
            api_key="<INSERT>",
            api_secret="<INSERT>>",
        )

    async def create_room(self, name):
        room_info = await self.lkapi.room.create_room(
            api.CreateRoomRequest(name=name),
        )
        return room_info
    
    async def list_rooms(self) -> list[str]:
        results = await self.lkapi.room.list_rooms(api.ListRoomsRequest())
        return [room.name for room in results.rooms]
    
    async def delete_room(self, room_name):
        await self.lkapi.room.delete_room(api.DeleteRoomRequest(room=room_name))
    
    async def get_user_in_room(self, room_name):
        users = await self.lkapi.room.list_participants(api.ListParticipantsRequest(room=room_name))
        return [user.identity for user in users.participants]
    
    async def kick_user_from_room(self, room_name, user_id):
        await self.lkapi.room.remove_participant(api.RoomParticipantIdentity(
            room=room_name,
            identity=user_id))
    
    def create_subscriber_token(self, user_id, user_name, room_name):
        token = (
            api.AccessToken()
            .with_identity(user_id)
            .with_name(user_name)
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=room_name,
                    can_publish=False,
                    can_subscribe=True,
                    can_publish_data=True,
                    hidden=True,
                )
            )
            .to_jwt()
        )
        return token
    
    def create_publisher_token(self, telescope_name, room_name):
        token = (
            api.AccessToken()
            .with_identity("telescope")
            .with_name(telescope_name)
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=room_name,
                    can_publish=True,
                    can_subscribe=True,
                    can_publish_data=True
                )
            )
            .to_jwt()
        )
        return token
        
    async def close(self):
        await self.lkapi.aclose()



# async def main():
#     lkc = LiveKitController()
#
#     # Create a room
#     await lkc.create_room("my-room")
#
#     # List rooms
#     rooms = await lkc.list_rooms()
#     print("Rooms:")
#     print(rooms)
#
#     # Get users in room
#     users = await lkc.get_user_in_room("my-room")
#     print("Users in room:")
#     print(users)
#
#     token = lkc.create_publisher_token("telescope", "my-room")
#     print("Publisher token:")
#     print(token)
#
#     token = lkc.create_subscriber_token("watcher1", "Jan Kowalski", "my-room")
#     print("Subscriber token:")
#     print(token)
#
#     await lkc.close()
#
# asyncio.run(main())