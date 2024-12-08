# SkyShareAPI

SkyShareAPI is a FastAPI-based web service that allows users to manage and interact with telescopes remotely. It offers functionality such as adding new telescopes, updating existing ones, locking telescopes for usage, and deleting them when no longer in use. Additionally, it includes endpoints to view the status of telescopes and get detailed specifications.

## Features

- **Add a Telescope**: Users can add new telescopes with their specifications and location information.
- **Update a Telescope**: Users can update existing telescope details.
- **Delete a Telescope**: Users can delete a telescope from the system.
- **Get Telescope List**: Retrieve a list of available, reserved, and unavailable telescopes.
- **Get Telescope Details**: Get detailed specifications for a specific telescope.
- **Lock Telescope**: Lock a telescope for a user’s session to begin observing.
- **Periodic Cleanup**: Clean up unused telescopes periodically by checking if any are idle (not being used) for a certain period.

## Installation

To install and run this project, you need to have Python 3.7+ installed. Then, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/PW-ZGS-2/backend.git
    cd SkyShareAPI
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set the `DATABASE_URL` environment variable to your database URL. For example, if you're using PostgreSQL:
    ```bash
    export DATABASE_URL=postgresql://user:password@localhost/dbname
    ```

## Running the Application

To run the API server, execute the following command:

```bash
uvicorn app:app --reload
