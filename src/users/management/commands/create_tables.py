from django.core.management.base import BaseCommand

from users.custom_db import get_conn
from users.create_tables_ddl import CREATE_TABLES_CLAUSE


class Command(BaseCommand):
    help = 'Creates tables'

    def handle(self, *args, **options):
        conn = get_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLES_CLAUSE)
        print('Tables created')
