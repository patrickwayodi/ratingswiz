"""
URLs module for the Pages app.
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import AboutView, ContactView, DocsView, SiteHomeView


urlpatterns = [
    path("", SiteHomeView.as_view(), name="site_home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("docs/", DocsView.as_view(), name="docs_home"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
