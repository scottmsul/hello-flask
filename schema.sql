DROP TABLE IF EXISTS animals;

CREATE TABLE animals (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO animals (name) VALUES ('moose');
INSERT INTO animals (name) VALUES ('bear');
INSERT INTO animals (name) VALUES ('squirrel');
INSERT INTO animals (name) VALUES ('zebra');
