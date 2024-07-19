import datetime
import smtplib
import logging
import pytz
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email

from mailings.models import Mailing, Attempt


logger = logging.getLogger(__name__)


# def send_email(mailing, client):
#     try:
#         send_mail(
#             subject=mailing.subject,
#             message=mailing.body,
#             from_email=settings.SERVER_EMAIL,
#             recipient_list=[client.email],
#             fail_silently=False,
#         )
#
#         Attempt.objects.create(
#             mailing=mailing,
#             client=client,
#             attempt_date=datetime.datetime.now(datetime.timezone.utc),
#             status=True,
#         )
#     except smtplib.SMTPException as e:
#         Attempt.objects.create(
#             mailing=mailing,
#             client=client,
#             attempt_date=datetime.datetime.now(datetime.timezone.utc),
#             status=False,
#             server_response=str(e),
#         )

def send_email(mailing, client):
    try:
        # Валидация адреса электронной почты
        validate_email(client.email)

        # Отправка письма
        response = send_mail(
            subject=mailing.subject,
            message=mailing.body,
            from_email=settings.SERVER_EMAIL,
            recipient_list=[client.email],
            fail_silently=False,
        )

        # Проверка ответа от сервера (количество успешно отправленных писем)
        if response:
            status = True
            server_response = "Успешно отправлено"
        else:
            status = False
            server_response = "Не удалось отправить"

        # Логирование успешного ответа
        print(f"Server response for {client.email}: {server_response}")

    except ValidationError:
        status = False
        server_response = "Неверный адрес электронной почты"
        print(f"Validation error for {client.email}: {server_response}")

    except smtplib.SMTPRecipientsRefused as e:
        status = False
        server_response = "Почтовый ящик не существует: " + str(e)
        print(f"SMTP Recipients Refused for {client.email}: {server_response}")

    except smtplib.SMTPResponseException as e:
        status = False
        server_response = f"Ошибка SMTP: {e.smtp_code} - {e.smtp_error}"
        print(f"SMTP Response Exception for {client.email}: {server_response}")

    except smtplib.SMTPException as e:
        status = False
        server_response = str(e)
        print(f"SMTP Exception for {client.email}: {server_response}")

    # Запись попытки отправки письма
    Attempt.objects.create(
        mailing=mailing,
        client=client,
        attempt_date=datetime.datetime.now(datetime.timezone.utc),
        status=status,
        server_response=server_response,
    )


def print_time_job():
    time_zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(time_zone)
    logger.info("ready method in YourAppConfig is called")
    print(f"Current time: {now}")


def send_mails():
    moscow_tz = pytz.timezone('Europe/Moscow')
    datetime_now = datetime.datetime.now(moscow_tz)
    for mailing in Mailing.objects.filter(status='started'):
        if mailing.start_datetime <= datetime_now <= mailing.stop_datetime:
            for client in mailing.client.all():
                last_attempt = Attempt.objects.filter(mailing=mailing, client=client).order_by('-attempt_date').first()

                should_send = False
                if last_attempt:
                    delta = datetime_now - last_attempt.attempt_date
                    if mailing.periodicity == 'minute' and delta.total_seconds() >= 60:
                        should_send = True
                    elif mailing.periodicity == 'hour' and delta.total_seconds() >= 3600:
                        should_send = True
                    elif mailing.periodicity == 'daily' and delta.days >= 1:
                        should_send = True
                    elif mailing.periodicity == 'weekly' and delta.days >= 7:
                        should_send = True
                    elif mailing.periodicity == 'monthly' and delta.days >= 30:
                        should_send = True
                else:
                    should_send = True

                if should_send:
                    send_email(mailing, client)
                    print(f"Email sent to {client.email} for mailing {mailing.id} in time {datetime_now}.")
