from django.contrib.auth.views import LoginView
from django.urls import path
from .apps import UsersConfig
from .views import RegisterView, verify_email, PasswordResetView, logout_view, ProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),

]