from .models import MailingAttempt


# Пример функции для создания попытки рассылки
def create_mailing_attempt(mailing, client, status, server_response):
    attempt = MailingAttempt(
        mailing=mailing,
        client=client,
        status=status,
        server_response=server_response
    )
    attempt.save()
