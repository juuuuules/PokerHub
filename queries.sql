-- DROP TABLE users;

-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     email TEXT NOT NULL,
--     hash TEXT NOT NULL
-- );

-- INSERT INTO users (email, hash) VALUES ('admin@example.com', 25);

-- SELECT * FROM users

-- CREATE TABLE sessions (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     email TEXT NOT NULL,
--     winnings INTEGER NOT NULL,
--     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (user_id) REFERENCES users(id)
-- );

-- DROP TABLE hands;

-- CREATE TABLE hands (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     session_id INTEGER NOT NULL,
--     user_hand TEXT NOT NULL,
--     result TEXT NOT NULL,
--     pot_size TEXT NOT NULL,
--     FOREIGN KEY (user_id) REFERENCES users(id),
--     FOREIGN KEY (session_id) REFERENCES sessions(id)
-- ); 

-- DELETE FROM hands WHERE user_hand = "J5s";

INSERT INTO hands (user_id, user_hand, result, pot_size) VALUES (2, "AsKd", "WIN", 10.00);
-- INSERT INTO hands (user_id, session_id, user_hand, result, pot_size) VALUES (2, 1, "J10d", "WIN", "$10");
-- INSERT INTO hands (user_id, session_id, user_hand, result, pot_size) VALUES (2, 1, "77", "WIN", "$10");

-- DELETE FROM hands WHERE pot_size = "$10$";

-- CREATE TABLE hands (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     user_hand TEXT NOT NULL,
--     result TEXT NOT NULL,
--     pot_size DECIMAL NOT NULL,
--     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (user_id) REFERENCES users(id)
-- );


-- CREATE TABLE hands (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     user_hand TEXT NOT NULL,
--     result TEXT NOT NULL,
--     pot_size DECIMAL NOT NULL,
--     FOREIGN KEY (user_id) REFERENCES users(id)
-- );

