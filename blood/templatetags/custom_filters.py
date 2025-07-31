from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to safely get a value from a dictionary.
    Usage: {{ dict|get_item:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    return 0

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Template filter to add a CSS class to a form field.
    Usage: {{ form.field|add_class:"form-control" }}
    """
    try:
        return field.as_widget(attrs={"class": css_class})
    except AttributeError:
        return field  # Return as-is if it's not a form field

@register.filter
def multiply(value, arg):
    """
    Template filter to multiply a value by an argument.
    Usage: {{ value|multiply:450 }}
    Removes .0 if result is a whole number.
    """
    try:
        result = float(value) * float(arg)
        if result.is_integer():
            return int(result)
        return result
    except (ValueError, TypeError):
        return 0