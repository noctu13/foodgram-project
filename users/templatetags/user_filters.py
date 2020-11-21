from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def next(lst, index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return lst[int(index) + 1]
    except IndexError:
        return ''
