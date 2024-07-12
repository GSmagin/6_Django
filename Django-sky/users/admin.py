from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'avatar', 'phone_number', 'country', 'last_login', 'token', 'is_active', 'is_superuser', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'avatar', 'phone_number', 'country', 'token')}),
        ('Permissions', {'fields': ('is_manager', 'is_active', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'avatar', 'phone_number', 'country', 'token',
                       'is_manager', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
