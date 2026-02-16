"""
Models for the "ratingLists" app
"""

import uuid

from random import random

from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse


class Post(models.Model):

    uploaded_file = models.FileField(upload_to="posts", verbose_name="File")

    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    owner = models.CharField(max_length=100, blank=True, null=True)

    unzipped_file_name = models.CharField(max_length=100, blank=True, null=True)

    release_date = models.DateField(unique=True, blank=True, null=True)

    player_total = models.IntegerField(blank=True, null=True)

    is_extracted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

    def __str__(self):
        return self.uploaded_file.name


class RatingList(models.Model):

    uploaded_file = models.FileField(
        upload_to="ratinglists",
        verbose_name="File",
        blank=True,
        null=True,
    )

    slug = models.SlugField(max_length=50, blank=True, null=True)

    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    owner = models.CharField(max_length=100, blank=True, null=True)

    original_file_name = models.CharField(max_length=100, blank=True, null=True)

    release_date = models.DateField(unique=True, blank=True, null=True)

    player_total = models.IntegerField(blank=True, null=True)

    has_player_profiles = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("rating_list_detail", args=[str(self.release_date)])

    def __str__(self):
        if self.original_file_name:
            return self.original_file_name
        else:
            return self.uploaded_file.name


class PlayerProfile(models.Model):

    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_created = models.DateField(auto_now_add=True)
    rating_list = models.ForeignKey(RatingList, on_delete=models.CASCADE)
    rating_date = models.DateField()
    index = models.IntegerField(blank=True, null=True)  # Position on the rating list
    slug = models.CharField(max_length=100, blank=True, null=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    fideid = models.CharField(max_length=100, blank=True, null=True)
    rating = models.CharField(max_length=100, blank=True, null=True)
    kfactor = models.IntegerField(blank=True, null=True)
    games = models.IntegerField(blank=True, null=True)
    birthday = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    w_title = models.CharField(max_length=100, blank=True, null=True)
    o_title = models.CharField(max_length=100, blank=True, null=True)
    foa_title = models.CharField(max_length=100, blank=True, null=True)
    flag = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                'fideid',
                'rating_date',
                name='unique_fideid_and_rating_date',
            ),
        ]

    def get_absolute_url(self):
        return reverse("player_profile_detail", args=[str(self.slug)])

    def __str__(self):
        return self.name


class FederationProfile(models.Model):

    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    owner = models.CharField(max_length=100, blank=True, null=True)

    federation_code = models.CharField(max_length=5, blank=True, null=True)

    player_total = models.CharField(max_length=100, blank=True, null=True)

    rating_date = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                'federation_code',
                'rating_date',
                name='unique_federation_code_and_rating_date',
            ),
        ]

    def get_absolute_url(self):
        return reverse("federation_profile_detail", args=[str(self.id)])

    def __str__(self):
        return self.federation_code + self.player_total


class FederationList(models.Model):

    uploaded_file = models.FileField(
        # upload_to="pgnfiles/%Y/%m/%d/",
        upload_to="uploadedfiles",
        verbose_name="File",
        blank=True,
        null=True,
    )

    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # owner = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)

    file_name = models.CharField(max_length=100, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("federation_list_detail", args=[str(self.id)])

    def __str__(self):
        # return self.blob_file.name
        return self.uploaded_file.name


class Region(models.Model):

    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # owner = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)

    player_total = models.CharField(max_length=100, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("federation_profile_detail", args=[str(self.id)])

    def __str__(self):
        # return self.blob_file.name
        return self.uploaded_file.name

