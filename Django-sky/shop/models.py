from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


# class PublishedProductManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_published='published')
#
#
# class UnpublishedProductManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_published='draft')


class Product(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'В архиве'),
    ]

    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес товара', null=True, blank=True)
    image = models.ImageField(upload_to='shop/', verbose_name='Изображение (превью)', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор')
    is_published = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статуса публикации')
#    manufactured_at = models.DateField(verbose_name='Дата производства')

    # published = PublishedProductManager()
    # unpublished = UnpublishedProductManager()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']
        permissions = [
            ('can_edit_product_publication', 'Can edit product publication'),
            ('can_edit_product_description', 'Can edit product description'),
            ('can_edit_product_category', 'Can edit product category'),
        ]

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.CASCADE, verbose_name="Продукт")
    version_number = models.CharField(max_length=50, verbose_name="Номер версии")
    version_name = models.CharField(max_length=255, verbose_name="Название версии")
    is_current = models.BooleanField(default=False, verbose_name="Текущая версия")

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        constraints = [
            # models.UniqueConstraint(fields=['product', 'version_name'], name='unique_version_name_per_product'),
            models.UniqueConstraint(fields=['product', 'version_name', 'version_number'],
                                    name='unique_version_per_product')
        ]

    def __str__(self):
        return f'{self.version_name} ({self.version_number})'


