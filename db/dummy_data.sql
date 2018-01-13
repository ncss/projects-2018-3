INSERT INTO users VALUES (
    'james',
    'password',
    'My name is James',
    'NSW',
    '15/1/2018',
    '/file/img.png'
);

INSERT INTO users VALUES (
    'jack',
    '123456',
    'My name is Jack',
    'NSW',
    '17/1/2018',
    ''
);

INSERT INTO squads VALUES (
    'jenga',
    6,
    '20/1/2018',
    '25/1/2018',
    'Come play jenga with me!',
    'IT Labs',
    'james',
    '12:00'
);

INSERT INTO squads VALUES (
    'ateam',
    10,
    '20/1/2018',
    '25/1/2018',
    'This is a team',
    'IT Labs',
    'james',
    '12:00'
);

INSERT INTO squad_members VALUES (
    'aaa', --Event id
    'James', --User id
    0,
    '1/1/2018'
);

INSERT INTO squad_members VALUES (
    'aaa',
    'Jack',
    1,
    '1/1/2018'
);
