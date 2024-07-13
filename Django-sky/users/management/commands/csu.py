from users.models import CustomUser
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = CustomUser.objects.create(email='admin@example.com')
        user.set_password('admin')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


