from django import template

register = template.Library()


@register.filter()
def bootstrap_size_css(value):
    if value in ["xs", "sm"]:
        return "d-block d-md-none w-100"
    elif value == "md":
        return "d-none d-md-block d-lg-none w-100"
    elif value in ["lg", "xl"]:
        return "d-none d-lg-block w-100"
    return ""
