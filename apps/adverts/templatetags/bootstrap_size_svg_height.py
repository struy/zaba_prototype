from django import template

register = template.Library()


@register.filter()
def bootstrap_size_svg_height(value):
    if value in ["xs", "sm"]:
        return "176"
    elif value == "md":
        return "176"
    elif value in ["lg", "xl"]:
        return "176"
    return "0"
