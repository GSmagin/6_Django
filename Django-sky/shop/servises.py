from django.core.cache import cache
from config.settings import CACHE_ENABLED

from shop.models import Product


def get_shop_from_cache():
    """"Получает данные товара из кеша если кеш не пуст, получает данные из БД"""
    if CACHE_ENABLED:
        return Product.objects.all()
    key = 'product_list'
    cache_product = cache.get(key)
    if cache_product is None:
        return cache_product
    cache_product = Product.objects.all()
    cache.set(key, cache_product)
    return cache_product

