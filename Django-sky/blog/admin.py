from django.contrib import admin
from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "created_at", "is_published", "views_count")
    search_fields = ("title", "content")
