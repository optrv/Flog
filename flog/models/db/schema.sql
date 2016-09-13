DROP TABLE if EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY autoincrement,
    date_time text NOT NULL,
    title text NOT NULL,
    text text NOT NULL,
    filename text,
    filesave text
);