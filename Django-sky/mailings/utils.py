from django.conf import settings
from datetime import datetime, timedelta
import pytz


def print_time_job():
    time_zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(time_zone)
    print(f"Current time: {now}")
# def send_mailing():
#     time_zone = pytz.timezone(settings.TIME_ZONE)
#     now = datetime.now(time_zone)
#     mailings = Mailing.objects.filter(status__in=['create', 'started'], start_time__gte=now-timedelta(minutes=5), start_time__lt=now)
#     for mailing in mailings:
#         if mailings.periodicity == 'everyday':
#             pass
#         elif mailings.periodicity == 'week' and (now - mailing.start_time).days % 7 == 0:
#             pass
#         elif mailings.periodicity == 'month' and (now - mailing.start_time).days % 30 == 0:
#             pass
