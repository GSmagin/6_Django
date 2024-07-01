from mailings.utils import print_time_job
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print_time_job()
