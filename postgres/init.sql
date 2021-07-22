CREATE DATABASE bot;

CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    user TEXT NOT NULL,
    quote TEXT NOT NULL,
)

CREATE TABLE infractions (
    id SERIAL PRIMARY KEY,
    user TEXT NOT NULL,
    type TEXT NOT NULL,
    reason TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    expires TIMESTAMP NOT NULL,
)