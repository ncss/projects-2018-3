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
    '12:00:00'
);

INSERT INTO squads VALUES (
    'ateam',
    10,
    '20/1/2018',
    '25/1/2018',
    'This is a team',
    'IT Labs',
    'james',
    '12:00:01'
);

INSERT INTO squad_members VALUES (
    'jenga', --Event id
    'james', --User id
    0,
    '1/1/2018'
);

INSERT INTO squad_members VALUES (
    'ateam',
    'jack',
    1,
    '1/1/2018'
);

INSERT INTO squad_messages VALUES (
    'jenga',
    'james',
    'hello everyone.',
    '05:00:00'
);

INSERT INTO squad_messages VALUES (
    'jenga',
    'emily',
    'I love Jenga too!',
    '05:01:00'
);

INSERT INTO squad_messages VALUES (
    'jenga',
    'james',
    'omg I have friend',
    '05:02:00'
);
