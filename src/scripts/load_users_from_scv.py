import hashlib

from psycopg2.extras import execute_values

from users.custom_db import get_conn


def parse_line(line):
    # String example: Абрамов Роберт,2012-01-01,Воткинск
    parts = line.strip().split(',')
    if len(parts) != 3:
        return None
    full_name, birthdate, city = parts
    if ' ' not in full_name:
        return None
    last_name, first_name = full_name.split(' ', 1)

    gender = 'male'
    interests = 'example interest'
    password = f'{last_name.lower()}123'
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    return (first_name, last_name, birthdate, gender, interests, city, password_hash)


def load_users_from_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()

    users = []
    for line in lines:
        user = parse_line(line)
        if user:
            users.append(user)

    if not users:
        print("No data")
        return

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            query = """
                INSERT INTO users (first_name, last_name, birthdate, gender, interests, city, password_hash)
                VALUES %s
            """
            execute_values(cur, query, users)
        conn.commit()
        print(f"Succesfully added {len(users)} users.")
    finally:
        conn.close()

load_users_from_file('scripts/people.v2.csv')
