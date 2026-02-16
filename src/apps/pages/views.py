"""
https://learndjango.com/tutorials/django-file-and-image-uploads-tutorial
"""


import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, View

from .forms import ExperimentalForm
from .models import HomePage


class SiteHomeView(TemplateView):

    template_name = "pages/site_home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["latest_articles"] = HomePage.objects.all()[:5]

        return context


class AboutView(TemplateView):

    template_name = "pages/about.html"


class ContactView(TemplateView):

    template_name = "pages/contact.html"


class DocsView(View):

    def get(self, request):

        return render(request, "pages/docs_home.html", {"experimental_form": ExperimentalForm()})

