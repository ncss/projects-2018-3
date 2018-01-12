CREATE DATABASE squadify;

CREATE TABLE users (
    id INTEGER, 
    username TEXT,
    password TEXT, 
    description TEXT, 
    location TEXT, 
    birthdate TEXT, 
    image TEXT, 
    PRIMARY KEY(id),
    UNIQUE(username)
);

CREATE TABLE squads (
    id INTEGER, 
    name TEXT, 
    capacity INTEGER, 
    creationdate TEXT, 
    eventdate TEXT, 
    description TEXT, 
    location TEXT, 
    leader INTEGER, 
    PRIMARY KEY(id), 
    FOREIGN KEY(leader) REFERENCES users (id)
);

CREATE TABLE squad_members (
    id INTEGER,
    event_id INTEGER,
    user_id INTEGER,
    status TEXT,
    application_time TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(event_id) REFERENCES squads (id),
    FOREIGN KEY(user_id) REFERENCES users (id)
);
