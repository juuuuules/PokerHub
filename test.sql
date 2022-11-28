-- DROP TABLE users;

-- CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, hash TEXT NOT NULL);

-- INSERT INTO users (email, hash) VALUES ('admin@example.com', 25);

-- SELECT * FROM users

-- CREATE TABLE sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, email TEXT NOT NULL, winnings INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));

CREATE TABLE hands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    email TEXT NOT NULL,
    user_hand TEXT NOT NULL,
    RESULT TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
); 



