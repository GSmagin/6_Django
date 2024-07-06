from django.apps import AppConfig


class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'
    verbose_name = "Рассылки"

    # def ready(self):
    #     from mailings.commands.runapscheduler import send_mails
    #     send_mails()

    # def ready(self):
    #     import mailings.commands.signals

    # def ready(self):
    #     from mailings.commands.start_print import start
    #     start()
