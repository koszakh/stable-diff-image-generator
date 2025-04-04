# generation/management/commands/wait_for_db.py

import time
import os
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        db_host = os.environ.get('DB_HOST')
        db_port = os.environ.get('DB_PORT')
        max_retries = 30
        retries = 0

        while not db_conn and retries < max_retries:
            try:
                # Используем 'default' соединение из settings.py
                connections['default'].ensure_connection()
                db_conn = True # Соединение успешно установлено
            except OperationalError as e:
                self.stdout.write(f"Database ({db_host}:{db_port}) unavailable, waiting 1 second... ({e})")
                retries += 1
                time.sleep(1)
            except Exception as e:
                 self.stdout.write(f"An unexpected error occurred: {e}")
                 retries += 1
                 time.sleep(1)


        if db_conn:
            self.stdout.write(self.style.SUCCESS('Database available!'))
        else:
            self.stdout.write(self.style.ERROR(f'Could not connect to database after {max_retries} retries. Exiting.'))
            # Выход с ошибкой, чтобы docker-compose понял, что запуск не удался
            exit(1)