
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
    squadname TEXT,
    capacity INTEGER,
    creation_date TEXT,
    squad_date TEXT,
    description TEXT,
    location TEXT,
    leader TEXT,
    squad_time TEXT,
    PRIMARY KEY(squadname),
    FOREIGN KEY(leader) REFERENCES users (username)
);

CREATE TABLE IF NOT EXISTS squad_members (
    squadname TEXT,
    username TEXT,
    status INTEGER,
    application_time TEXT,
    FOREIGN KEY(squadname) REFERENCES squads (squadname),
    FOREIGN KEY(username) REFERENCES users (username)
);

CREATE TABLE IF NOT EXISTS squad_messages(
    squadname TEXT,
    sender_username TEXT,
    message TEXT,
    time_sent TEXT,
    PRIMARY KEY(squadname, time_sent),
    FOREIGN KEY(sender_username) REFERENCES users (username),
    FOREIGN KEY(squadname) REFERENCES squads (squadname)
);
