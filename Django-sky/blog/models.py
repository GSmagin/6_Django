from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Заголовок поста")
    slug = models.CharField(max_length=150, verbose_name="Ссылка для поста")
    content = models.TextField(verbose_name="Содержимое поста")
    preview_image = models.ImageField(upload_to="blog/", verbose_name="Превью поста (изображение)", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_at']
