DROP TABLE if EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY autoincrement,
    title text NOT NULL,
    text text NOT NULL
);