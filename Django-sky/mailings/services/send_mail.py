import datetime
import smtplib

from django.conf import settings
from django.core.mail import send_mail

from mailings.models import Mailing, Attempt


def send_email(message_settings, message_client):
    try:
        send_mail(
            subject=message_settings.message.title,
            message=message_settings.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[message_client.email],
            fail_silently=False,
        )

        Attempt.objects.create(
            time=datetime.datetime.now(datetime.timezone.utc),
            status="Успешно",
            mailing_list=message_settings,
        )
    except smtplib.SMTPException as e:
        Attempt.objects.create(
            time=datetime.datetime.now(datetime.timezone.utc),
            status="Ошибка",
            server_response=str(e),
            mailing_list=message_settings,
        )


def send_mails():
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    for mailing_setting in Mailing.objects.filter(status=Mailing.started):

        if (datetime_now > mailing_setting.start_time) and (datetime_now < mailing_setting.end_time):

            for mailing_client in mailing_setting.clients.all():
                mailing_log = Attempt.objects.filter(
                    client=mailing_client.pk,
                    settings=mailing_setting
                )

                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('- time').first().time

                    if mailing_setting.periodicity == Mailing.daily:
                        if (datetime_now - last_try_date).days >= 1:
                            send_email(mailing_setting, mailing_client)
                    elif mailing_setting.periodicity == Mailing.weekly:
                        if (datetime_now - last_try_date).days >= 7:
                            send_email(mailing_setting, mailing_client)
                    elif mailing_setting.periodicity == Mailing.monthly:
                        if (datetime_now - last_try_date).days >= 30:
                            send_email(mailing_setting, mailing_client)
                else:
                    send_email(mailing_setting, mailing_client)
