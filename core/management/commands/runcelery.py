import os
import signal
import subprocess
import time

import psutil
from django.core.management.base import BaseCommand
from django.utils import autoreload


DELAY_UNTIL_START = 5.0
CELERY_COMMAND = "celery -A leadanne2 worker --loglevel=INFO"


class Command(BaseCommand):
    help = ""

    def kill_celery(self, parent_pid):
        os.kill(parent_pid, signal.SIGTERM)

    def run_celery(self):
        time.sleep(DELAY_UNTIL_START)
        subprocess.run(CELERY_COMMAND.split(" "))

    def get_main_process(self):
        for process in psutil.process_iter():
            if process.ppid() == 0:  # PID 0 has no parent
                continue

            parent = psutil.Process(process.ppid())

            if process.name() == "celery" and parent.name() == "celery":
                return parent

        return

    def reload_celery(self):
        parent = self.get_main_process()

        if parent is not None:
            self.stdout.write("[*] Killing Celery process gracefully..")
            self.kill_celery(parent.pid)

        self.stdout.write("[*] Starting Celery...")
        self.run_celery()

    def handle(self, *args, **options):
        autoreload.run_with_reloader(self.reload_celery)
