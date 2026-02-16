from django import template
from django.conf import settings


register = template.Library()


def sitename(value):
    """Returns the website's name."""

    try:
        if settings.SITE_NAME=="":
            return value
        else:
            return settings.SITE_NAME
    except AttributeError:
        print("AttributeError: 'Settings' object has no attribute 'SITE_NAME'")

    return value


register.filter("sitename", sitename)

