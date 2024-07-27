from django.apps import AppConfig
import time


class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'
    verbose_name = "Рассылки"





    # def ready(self):
    #     import mailings.management.commands.start_print
    #     start()

    # def ready(self):
    #     from mailings.commands.runapscheduler import send_mails
    #     send_mails()

    # def ready(self):
    #     from mailings.management.commands.start_print import start
    #     start()

    # def ready(self):
    #     from mailings.commands.start_print import start
    #     start()

    # def ready(self):
    #     from mailings.management.commands.scheduler import start_scheduler
    #     start_scheduler()
    # def ready(self):
    #     import mailings.management.commands.signals
