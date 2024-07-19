from django.db import models
from django.utils import timezone
from django.utils.timezone import now

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="контактный email")
    full_name = models.CharField(max_length=250, verbose_name="ФИО")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Mailing(models.Model):
    minute = 'Раз в минуту'
    hour = 'Раз в час'
    daily = 'Раз в день'
    weekly = 'Раз в неделю'
    monthly = 'Раз в месяц'

    created = 'Создана'
    started = 'Запущена'
    finished = 'Завершена'

    PERIODICITY_CHOICES = [
        ('minute', 'Раз в минуту'),
        ('hour', 'Раз в час'),
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    start_datetime = models.DateTimeField(default=now, verbose_name="Дата создания")
    stop_datetime = models.DateTimeField(default=now, verbose_name="Дата окончания рассылки")
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, verbose_name="Периодичность")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name="Статус рассылки")
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Текст письма")
    client = models.ManyToManyField(Client, verbose_name='клиент')

    def __str__(self):
        return f"Рассылка {self.id} - {self.get_status_display()}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    attempt_date = models.DateTimeField(default=timezone.now, verbose_name="Дата попытки")
    status = models.BooleanField(default=False, verbose_name="Статус попытки")
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ сервера")

    def __str__(self):
        return f"Попытка {self.mailing.id} to {self.client.email} at {self.attempt_date}"

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'




