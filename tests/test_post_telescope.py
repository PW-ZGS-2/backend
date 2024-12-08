import pytest
from sqlalchemy.orm import Session

from telescope.db_models import TelescopeDB
from telescope.handler import PostTelescopeHandler
from telescope.telescope_route import get_db
from unittest import mock

from tests.requests_stubs import post_telescope_stub


@pytest.fixture
def mock_livekit_controller():
    # Mock the LiveKitController class
    with mock.patch("telescope.livekit_controller.LiveKitController", autospec=True) as MockLiveKitController:
        # Create an instance of the mocked class
        mock_controller = MockLiveKitController.return_value

        # Mock the methods you want to control
        mock_controller.create_room.return_value = {"name": "test_room"}
        mock_controller.list_rooms.return_value = ["room1", "room2", "room3"]
        mock_controller.delete_room.return_value = None
        mock_controller.get_user_in_room.return_value = ["user1", "user2"]
        mock_controller.kick_user_from_room.return_value = None
        mock_controller.create_subscriber_token.return_value = "subscriber_token"
        mock_controller.create_publisher_token.return_value = "publisher_token"

        yield mock_controller

@pytest.fixture(scope="function")
def db_session():
    # Create a session and begin a transaction
    db = next(get_db())  # Assuming get_db provides a session
    db.begin()  # Start a transaction
    yield db
    db.rollback()  # Rollback at the end of the test
    db.close()


async def test_create_telescope(db_session: Session, mock_livekit_controller):
    # Create the handler instance with the mocked controller
    service = PostTelescopeHandler(db=db_session, controller=mock_livekit_controller)

    # Call the method to create a telescope
    response = await service.run(post_telescope_stub)

    # Query the database to check if the telescope was added
    telescope = db_session.query(TelescopeDB).filter(TelescopeDB.telescope_name == "Test Telescope").first()

    # Assert that the telescope was added to the database
    assert telescope is not None
    assert telescope.telescope_name == "Test Telescope"

    # Assert that the response status is success (based on your code structure)
    assert response.status == "success"

    # Check if the LiveKitController's methods were called
    mock_livekit_controller.create_room.assert_called_once_with("Test Telescope")
    mock_livekit_controller.create_publisher_token.assert_called_once_with("Test Telescope", "test_room")
