"""
Views for the "ratinglists" Django app.
"""

import csv
import datetime
import gc
import io
import json
import logging
import os
import subprocess
import xml.etree.ElementTree as ET

from io import BytesIO
from zipfile import ZipFile

from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, View

from .controllers import create_fed_profile
from .controllers import create_rating_list
from .controllers import create_region_profile
from .controllers import get_top_20_players

from .forms import RatingListForm
from .forms import PostForm

from .models import FederationList
from .models import FederationProfile
from .models import PlayerProfile
from .models import Post
from .models import RatingList
from .models import Region


class PostCreateView(CreateView):

    model = Post

    form_class = PostForm

    template_name = "ratinglists/create_post.html"


class PostDetailView(DetailView):

    template_name = "ratinglists/post_detail.html"

    model = Post

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["post"] = get_object_or_404(Post, pk=self.kwargs["pk"])

        return context


class PostListView(ListView):

    model = Post

    template_name = "ratinglists/post_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["posts"] = Post.objects.order_by("-id")[:50]

        return context


class RatingListCreateView(View):

    def get(self, request, pk):

        print("\n    Debugging RatingListCreateView()")

        # post = get_object_or_404(Post, id=post_pk)
        post = get_object_or_404(Post, pk=pk)

        if post.is_extracted:
            print("\n    Error: The rating list had already been processed.\n\n")
            print("\n    Finishing create_rating_list() \n\n")
            return render(
                request,
                "ratinglists/create_rating_list_error.html",
                {"post": post},
            )
        else:
            rating_list = create_rating_list(pk)

        print("\n    Ending RatingListCreateView() \n\n")

        return render(
            request,
            "ratinglists/create_rating_list.html",
            {"post": post, "rating_list": rating_list},
        )


class RatingListDetailView(View):

    def get(self, request, date):

        print("\n\n    Debugging RatingListDetailView()")

        rating_list = "jan13frl"

        rating_list = get_object_or_404(RatingList, release_date=date)

        federations = []
        for fed in settings.FIDE_FEDERATIONS:
            federations.append((fed["name"], fed["code"]))

        print("\n    Ending RatingListDetailView() \n\n")

        return render(
            request,
            "ratinglists/rating_list_detail.html",
            {"rating_list": rating_list, "rating_date": date, "federations": federations},
        )


class RatingListListView(View):

    def get(self, request):

        print("\n    Debugging RatingListListView()")

        rating_lists = ["jan13frl", "feb13frl",]

        rating_lists = RatingList.objects.order_by("-id")[:50]

        print("\n    Ending RatingListListView()")

        return render(
            request,
            "ratinglists/rating_list_list.html",
            {"rating_lists": rating_lists},
        )


class FederationDetailView(View):

    def get(self, request, fed, date):

        print("\n    Debugging FederationDetailView()")

        fed_profile = create_fed_profile(fed, date)

        print("\n    Ending FederationDetailView()")

        return render(
            request, "ratinglists/federation_detail.html", {"fed_profile": fed_profile},
        )


class FederationListView(View):

    def get(self, request, fed):

        print("\n    Debugging FederationListView()")

        rating_list = "jan13frl"

        print("\n    Ending FederationListView()")

        return render(
            request,
            "ratinglists/federation_list.html",
            {"rating_list": rating_list},
        )


class FedTop20PlayersView(View):
    """
    TODO: controllers.create_fed_profile(rating_list_pk, fed)
    """

    def get(self, request, fed, date):

        print("\n    Debugging FedTop20PlayersView()")

        players = get_top_20_players(fed, date)

        print("\n    Ending FedTop20PlayersView()")

        return render(
            request,
            "ratinglists/top_10_players.html",
            {
                "rating_date": players["rating_date"],
                "all_players": players["all_players"],
                "veterans": players["veterans"],
                "youngbloods": players["youngbloods"],
                "ladies": players["ladies"],
                "junior_boys": players["junior_boys"],
                "junior_girls": players["junior_girls"],
                "under_12_boys": players["under_12_boys"],
                "under_12_girls": players["under_12_girls"],
                "under_8": players["under_8"],
                "top_1960s": players["top_1960s"],
                "top_1970s": players["top_1970s"],
                "top_1980s": players["top_1980s"],
                "top_1990s": players["top_1990s"],
                "top_2000s": players["top_2000s"],
                "top_2010s": players["top_2010s"],
            },
        )


class RegionDetailView(View):

    def get(self, request, name):

        print("\n    Debugging RegionDetailView()")

        region_profile, chart_image = create_region_profile(name)

        print("\n    Ending RegionDetailView() \n\n")

        return render(
            request, "ratinglists/region_detail.html",
            {"region": region_profile, "name": name, "chart": chart_image},
        )


class RegionDetailCSVView(View):

    def get(self, request, name):

        print("\n    Debugging RegionDetailCSVView()")

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="region-ratings.csv"'},
        )

        writer = csv.writer(response)

        region, chart_image = create_region_profile(name)

        writer.writerow([
            "", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
            "2021", "2022", "2023", "2024", "2025", "2026"
        ])

        for federation in region:
            # writer.writerow(["First row", "Foo", "Bar", "Baz"])
            # writer.writerow(["Second row", "A", "B", '"Testing"', "Here's a quote"])
            writer.writerow(federation)

        print("\n    Ending RegionDetailCSVView() \n\n")

        return response


class RegionListView(View):

    def get(self, request, fed):

        print("\n    Debugging RegionListView()")

        rating_list = "jan13frl"

        print("\n    Ending RegionListView()")

        return render(
            request,
            "ratinglists/region_list.html",
            {"rating_list": rating_list},
        )


class RegionGrowthView(View):

    def get(self, request, fed):

        print("\n    Debugging RegionGrowthView()")

        rating_list = "jan13frl"

        print("\n    Ending RegionGrowthView()")

        return render(
            request,
            "ratinglists/region_growth.html",
            {"rating_list": rating_list},
        )


class RatingListProcessorView(View):

    def get(self, request, pk):
        print("\n\n    Debugging RatingListProcessorView()")

        rating_list_pk = pk
        rating_list = get_object_or_404(RatingList, pk=rating_list_pk)
        uploaded_file = rating_list.uploaded_file

        rating_list_zipped = ZipFile(uploaded_file, "r")
        rating_list_name = rating_list_zipped.namelist()[0]
        rating_list_data = rating_list_zipped.read(rating_list_name)
        rating_list_file = BytesIO(rating_list_data)

        # https://www.iditect.com/faq/python/using-python-iterparse-for-large-xml-files.html
        # https://web.archive.org/web/20201111201837/http://effbot.org/zone/element-iterparse.htm#incremental-parsing
        total = 0
        for event, elem in ET.iterparse(rating_list_file, events=("end",)):
            if elem.tag == "player":
                total = total + 1
                elem.clear()  # Free the memory
        print("\n    Total players: ", total)

        rating_list.original_file_name = rating_list_name
        rating_list.player_total = total
        release_date = get_rating_date(rating_list_name)
        rating_list.release_date = release_date
        rating_list.slug = release_date
        rating_list.save()

        messages.add_message(request, messages.INFO, "Details updated")

        print("\n    Finishing RatingListProcessorView() \n\n")

        # return HttpResponseRedirect(
            # reverse_lazy("rating_list_detail", kwargs={"slug": release_date})
        # )
        return render(
            request,
            "ratinglists/rating_list_processor.html",
            {"release_date": release_date},
        )


class PlayerProfileDetailView(DetailView):

    template_name = "ratinglists/player_profile_detail.html"

    model = PlayerProfile

    def get_context_data(self, **kwargs):
        print("\n    Debugging PlayerProfileDetailView() \n\n")

        context = super().get_context_data(**kwargs)

        release_date = self.kwargs["slug"][:10]
        print("\n\n    release_date:", release_date, "\n\n")

        index=self.kwargs["slug"][11:]
        print("\n\n    index:", index, "\n\n")

        rating_list = get_object_or_404(RatingList, release_date=release_date)
        print("\n\n    rating_list:", rating_list.id, "\n\n")

        player_profile = get_object_or_404(PlayerProfile, rating_list=rating_list.id, index=index)
        print("\n\n    player_profile:", player_profile.id, "\n\n")

        context["player_profile"] = player_profile

        print("\n    Finishing PlayerProfileDetailView() \n\n")

        return context


class PlayerProfileListView(ListView):

    model = PlayerProfile

    template_name = "ratinglists/player_profile_list.html"

    def get_queryset(self, **kwargs):

        queryset = PlayerProfile.objects.order_by("-id")[:50]

        return queryset

    def get_context_data(self, **kwargs):
        print("\n    Debugging PlayerProfileListView() \n\n")

        context = super(PlayerProfileListView, self).get_context_data(**kwargs)

        context["player_profiles"] = PlayerProfile.objects.order_by("-id")[:50]

        print("\n    Finishing PlayerProfileListView() \n\n")

        return context

