from contextlib import contextmanager

import psycopg2
from psycopg2 import pool

from django.conf import settings


conn_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=4,
    dbname=settings.DATABASES['default']['NAME'],
    user=settings.DATABASES['default']['USER'],
    password=settings.DATABASES['default']['PASSWORD'],
    host=settings.DATABASES['default']['HOST'],
    port=settings.DATABASES['default']['PORT'],
)


@contextmanager
def get_conn():
    conn = conn_pool.getconn()
    try:
        yield conn
    finally:
        conn_pool.putconn(conn)


def create_user(data):
    with get_conn() as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (first_name, last_name, birthdate, gender, interests, city, password_hash)
                    VALUES (%s, %s, %s, %s, %s, %s, crypt(%s, gen_salt('bf')))
                    RETURNING id
                """, (data['first_name'], data['last_name'], data['birthdate'], data['gender'], data['interests'], data['city'], data['password']))
                return cur.fetchone()[0]


def get_user(user_id):
    with get_conn() as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, first_name, last_name, birthdate, gender, interests, city FROM users WHERE id = %s", (user_id,))
                row = cur.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'first_name': row[1],
                        'last_name': row[2],
                        'birthdate': row[3],
                        'gender': row[4],
                        'interests': row[5],
                        'city': row[6],
                    }


def check_password(first_name, password):
    with get_conn() as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE first_name = %s AND password_hash = crypt(%s, password_hash)", (first_name, password))
                row = cur.fetchone()
                return row[0] if row else None


def search_users(first_name_prefix, last_name_prefix):
    with get_conn() as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, first_name, last_name, birthdate, gender, interests, city
                    FROM users
                    WHERE first_name LIKE %s AND last_name LIKE %s
                    ORDER BY id
                """, (f"{first_name_prefix}%", f"{last_name_prefix}%"))
                return cur.fetchall()
