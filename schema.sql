-- This file should contain all code required to create & seed database tables.

DROP DATABASE IF EXISTS museum;

CREATE DATABASE museum;

\c museum;

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    dept_name TEXT NOT NULL
);

CREATE TABLE floors (
    id SERIAL PRIMARY KEY,
    floor_name TEXT NOT NULL
);

CREATE TABLE exhibitions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    department_id INT,
    floor_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (floor_id) REFERENCES floors(id)
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    value INT NOT NULL CHECK (value BETWEEN 0 AND 4),
    description TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    at TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    exhibition_id INT,
    rating_id INT,
    FOREIGN KEY (exhibition_id) REFERENCES exhibitions(id),
    FOREIGN KEY (rating_id) REFERENCES ratings(id),
    UNIQUE (at, exhibition_id, rating_id)
);

CREATE TABLE emergencies (
    id SERIAL PRIMARY KEY,
    at TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    exhibition_id INT,
    FOREIGN KEY (exhibition_id) REFERENCES exhibitions(id),
    UNIQUE (at, exhibition_id)
);

CREATE TABLE assistances (
    id SERIAL PRIMARY KEY,
    at TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    exhibition_id INT,
    FOREIGN KEY (exhibition_id) REFERENCES exhibitions(id),
    UNIQUE (at, exhibition_id)
);

INSERT INTO departments(dept_name)
    VALUES 
    ('Entomology'),
    ('Geology'),
    ('Paleontology'),
    ('Zoology'),
    ('Ecology')
;

INSERT INTO floors(floor_name)
    VALUES 
    ('Vault'),
    ('1'),
    ('2'),
    ('3')
;

INSERT INTO ratings(value, description)
    VALUES 
    (0, 'Terrible'),
    (1, 'Bad'),
    (2, 'Neutral'),
    (3, 'Good'),
    (4, 'Amazing')
;

INSERT INTO exhibitions(name, description, start_date, department_id, floor_id)
    VALUES 
        ('Measureless to Man',
        'An immersive 3D experience: delve deep into a previously-inaccessible cave system.',
        '2021-08-23',
        2,
        2),

        ('Adaptation',
        'How insect evolution has kept pace with an industrialised world',
        '2019-07-01',
        1,
        1),

        ('The Crenshaw Collection',
        'An exhibition of 18th Century watercolours, mostly focused on South American wildlife.',
        '2021-03-03',
        4,
        3),

        ('Cetacean Sensations',
        'Whales: from ancient myth to critically endangered.',
        '2019-07-01',
        4,
        2),

        ('Our Polluted World',
        'A hard-hitting exploration of humanity''s impact on the environment.',
        '2021-05-12',
        5,
        4),

        ('Thunder Lizards',
        'How new research is making scientists rethink what dinosaurs really looked like.',
        '2023-02-01',
        3,
        2)
;