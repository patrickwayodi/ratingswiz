"""
https://docs.djangoproject.com/en/4.2/ref/models/fields
https://docs.djangoproject.com/en/4.2/ref/models/fields/#datetimefield
"""


from django.db import models
from django.urls import reverse


class HomePage(models.Model):

    # owner = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)

    introduction = models.TextField(
        max_length=500,
        verbose_name="Introduction",
    )

    summary = models.TextField(
        max_length=500,
        verbose_name="Summary",
    )

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):

        return self.request_url

