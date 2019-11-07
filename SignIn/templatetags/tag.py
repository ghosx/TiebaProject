from django import template
import datetime
register = template.Library()

@register.simple_tag(name="date_tag")
def add_simpletag():
    return datetime.datetime.now().strftime("%Y")