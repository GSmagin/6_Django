from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from mailings.utils import print_time_job
from django.core.management.base import BaseCommand


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        print_time_job,
        trigger=IntervalTrigger(minutes=1),
        id="print_time_minute",
        max_instances=1,
        replace_existing=True,
    )

    scheduler.start()
