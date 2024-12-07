-- Table to store location data
CREATE TABLE Locations (
    id UUID PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(10),
    latitude FLOAT,
    longitude FLOAT
);

-- Table to store user data
CREATE TABLE Users (
    id UUID PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    second_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    address TEXT
);

-- Table to store telescope specifications
CREATE TABLE TelescopeSpecifications (
    id UUID PRIMARY KEY,
    aperture FLOAT NOT NULL,
    focal_length FLOAT NOT NULL,
    focal_ratio FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    length FLOAT NOT NULL,
    width FLOAT NOT NULL,
    height FLOAT NOT NULL,
    mount_type VARCHAR(50) NOT NULL,  -- Changed from UUID to VARCHAR for mount type
    optical_design VARCHAR(50) NOT NULL  -- Changed from UUID to VARCHAR for optical design
);

-- Table to store telescopes
CREATE TABLE Telescopes (
    id UUID PRIMARY KEY,
    telescope_name VARCHAR(100),
    telescope_type VARCHAR(50) NOT NULL,  -- Changed from UUID to VARCHAR for telescope type
    price_per_minute FLOAT,
    owner VARCHAR(100),
    status VARCHAR(50) NOT NULL,  -- Changed from UUID to VARCHAR for status
    location_id UUID NOT NULL,
    specifications_id UUID NOT NULL,
    FOREIGN KEY (location_id) REFERENCES Locations(id),
    FOREIGN KEY (specifications_id) REFERENCES TelescopeSpecifications(id)
);

CREATE TABLE TelescopeStates (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    telescope_id UUID NOT NULL,
    action_time TIMESTAMP NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (telescope_id) REFERENCES Telescopes(id)
);

CREATE TABLE room (
    room_id UUID PRIMARY KEY,                -- Primary key for the Room table
    telescope_id UUID,                      -- Foreign key linking to the Telescope table
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Time when the room was created
    publisher_key VARCHAR(800) NOT NULL,    -- Publisher key for the room
    FOREIGN KEY (telescope_id) REFERENCES telescopes(id)  -- Define foreign key constraint
);