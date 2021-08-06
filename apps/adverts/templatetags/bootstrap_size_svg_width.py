from django import template

register = template.Library()


@register.filter()
def bootstrap_size_svg_width(value):
    if value in ["xs", "sm"]:
        return "720"
    elif value == "md":
        return "800"
    elif value in ["lg", "xl"]:
        return "1000"
    return "0"
