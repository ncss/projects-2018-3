
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT, 
    description TEXT, 
    location TEXT, 
    birthdate TEXT, 
    image TEXT, 
    PRIMARY KEY(username)
);

CREATE TABLE IF NOT EXISTS squads (
    name TEXT, 
    capacity INTEGER, 
    creationdate TEXT, 
    eventdate TEXT, 
    description TEXT, 
    location TEXT, 
    leader INTEGER, 
    PRIMARY KEY(name), 
    FOREIGN KEY(leader) REFERENCES users (username)
);

CREATE TABLE IF NOT EXISTS squad_members (
    event_name TEXT,
    user_name TEXT,
    status TEXT,
    application_time TEXT,
    FOREIGN KEY(event_name) REFERENCES squads (name),
    FOREIGN KEY(user_name) REFERENCES users (username)
);
