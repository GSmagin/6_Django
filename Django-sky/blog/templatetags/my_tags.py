from django import template

register = template.Library()


@register.filter()
def media_files(path):
    if path:
        return f"/media/{path}"
    return "/media/no_foto.jpg"


@register.filter
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value
