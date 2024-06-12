
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_date_ddmmyyyy(value):
    try:
        date_obj = datetime.strptime(value, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return value