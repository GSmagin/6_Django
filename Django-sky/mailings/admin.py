from django.contrib import admin
from .models import Client, Mailing, Attempt

admin.site.register(Client)
admin.site.register(Mailing)
# admin.site.register(Message)
admin.site.register(Attempt)
