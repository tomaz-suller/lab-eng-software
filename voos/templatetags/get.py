from django import template

register = template.Library()


@register.filter
def get(obj, attribute_name: str):
    try:
        return getattr(obj, attribute_name)
    except AttributeError:
        try:
            return obj[attribute_name]
        except KeyError:
            ...

    return None
