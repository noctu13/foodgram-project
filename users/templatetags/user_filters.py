from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def tag_query(query, item):
    """
    Returns href query for Tags items
    Depends on Tag model
    """
    href = '?'
    for choice in query:
        if choice != item:
            href += 'tag=' + choice.name + '&'
    return href[:-1]
