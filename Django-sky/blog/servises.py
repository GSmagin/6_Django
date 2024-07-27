from django.core.cache import cache
from config.settings import CACHE_ENABLED
from blog.models import Blog


def get_blog_from_cache():
    """"Получает данные блога из кеша если кеш не пуст, получает данные из БД"""
    if CACHE_ENABLED:
        return Blog.objects.all()
    key = 'blogpost_list'
    cache_blog = cache.get(key)
    if cache_blog is None:
        return cache_blog
    cache_blog = Blog.objects.all()
    cache.set(key, cache_blog)
    return cache_blog

