from django import template

register = template.Library()

@register.filter
def format_price(value):
    """
    Format price with thousands separator using dot (.)
    Example: 1200000 -> 1.200.000
    """
    try:
        # Convert to integer
        price = int(value)
        # Format with thousands separator
        return f"{price:,}".replace(',', '.')
    except (ValueError, TypeError):
        return value

@register.filter
def split_amenities(value):
    if value:
        return [item.strip() for item in value.split(',')]
    return []
