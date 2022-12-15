from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """Add the arg to the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        try:
            return value * arg
        except Exception:
            return ''
        
@register.filter
def due(value, arg):
    """Add the arg to the value."""
    try:
       
        result = int(value) - int(arg)
        
        if int(result) <= int(0):
            data = 0   
        else:
            data = result
        return data
    except (ValueError, TypeError):
        try:
            result2 = value - arg
            if result2 <= 0:
                data2 = 0
            else:
                data2 = result2
            return data2
        except Exception:
            return 0