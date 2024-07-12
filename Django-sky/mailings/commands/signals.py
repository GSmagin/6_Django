from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def execute_after_migrations(sender, **kwargs):
    from mailings.commands.runapscheduler import send_mails
    send_mails()
#
#
# @receiver(post_migrate)
# def execute_after_migrations2(sender, **kwargs):
#     from mailings.commands.start_print import start
#     start()


