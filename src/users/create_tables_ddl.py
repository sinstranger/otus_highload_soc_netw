CREATE_TABLES_CLAUSE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    birthdate DATE,
    gender TEXT,
    interests TEXT,
    city TEXT,
    password_hash TEXT
);
"""