INSERT INTO users VALUES (
    'James',
    'password',
    'My name is James',
    'NSW',
    '15/1/2018',
    '/file/img.png'
);

INSERT INTO users VALUES (
    'Jack',
    '123456',
    'My name is Jack',
    'NSW',
    '17/1/2018',
    ''
);

INSERT INTO squads VALUES (
    'ABCD',
    10,
    '20/1/2018',
    '25/1/2018',
    'This is a squad',
    'IT Labs',
    0,
    '12:00'
);

INSERT INTO squads VALUES (
    'ateam',
    10,
    '20/1/2018',
    '25/1/2018',
    'This is a team',
    'IT Labs',
    0,
    '12:00'
);

INSERT INTO squad_members VALUES (
    'James', --Event id
    'aaa', --User id
    0,
    '1/1/2018'
);

INSERT INTO squad_members VALUES (
    'Jack',
    'aaa',
    1,
    '1/1/2018'
);