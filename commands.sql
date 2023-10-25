CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER,
    task_string TEXT,
    completed BOOLEAN DEFAULT (FALSE),
    date_created DATETIME,
    date_completed DATETIME
);