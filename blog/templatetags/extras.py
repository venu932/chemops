from django import template

register=template.Library()

@register.filter(Name="get_val")
def get_val(dict, key):
    return dict.get(key)