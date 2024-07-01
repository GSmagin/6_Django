from django_apscheduler.jobstores import register_job, register_events
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.models import DjangoJobExecution
import logging

from .models import Mailing, Client, Attempt
from datetime import datetime
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_mailing():
    now = datetime.now()
    mailings = Mailing.objects.filter(start_datetime__lte=now, status='created')

    for mailing in mailings:
        clients = Client.objects.all()
        for client in clients:
            try:
                send_mail(
                    mailing.message_set.first().subject,
                    mailing.message_set.first().body,
                    'your_email@example.com',
                    [client.email],
                )
                status = 'success'
                response = 'Mail sent successfully'
            except Exception as e:
                status = 'failed'
                response = str(e)

            Attempt.objects.create(
                mailing=mailing,
                status=status,
                response=response
            )

        mailing.status = 'completed'
        mailing.save()


scheduler = BackgroundScheduler()
scheduler.add_jobstore('django_apscheduler.jobstores:DjangoJobStore')
scheduler.add_job(send_mailing, 'interval', minutes=1, id='send_mailing')
register_events(scheduler)

scheduler.start()
