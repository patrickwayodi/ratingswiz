"""
URL configuration for the "ratinglists" Django app.
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import PostCreateView
from .views import PostDetailView
from .views import PostListView

from .views import RatingListCreateView
from .views import RatingListDetailView
from .views import RatingListListView

from .views import FederationDetailView
from .views import FederationListView
from .views import FedTop20PlayersView

from .views import RegionDetailView
from .views import RegionDetailCSVView
from .views import RegionListView
from .views import RegionGrowthView

from .views import PlayerProfileListView
from .views import PlayerProfileDetailView
from .views import RatingListCreateView
from .views import RatingListProcessorView
from .views import RatingListDetailView
from .views import RatingListListView
from .views import FederationDetailView
from .views import FederationListView


urlpatterns = [
    path("post/new/", PostCreateView.as_view(), name="create_post",),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail",),
    path("posts/", PostListView.as_view(), name="post_list",),

    path("post/<int:pk>/extract/", RatingListCreateView.as_view(), name="create_rating_list",),
    path("ratinglist/<date>/", RatingListDetailView.as_view(), name="rating_list_detail",),
    path("ratinglists/", RatingListListView.as_view(), name="rating_list_list",),

    path("federation/<fed>/<date>/", FederationDetailView.as_view(), name="federation_detail",),
    path("federations/", FederationListView.as_view(), name="federation_list",),
    path("federation/<fed>/top-20/<date>/", FedTop20PlayersView.as_view(), name="fed_top_20_players",),

    path("region/<name>/", RegionDetailView.as_view(), name="region_detail",),
    path("region/<name>/csv/", RegionDetailCSVView.as_view(), name="region_detail_csv",),
    path("regions/", RegionListView.as_view(), name="region_list",),
    path("region/<name>/growth/", RegionGrowthView.as_view(), name="region_growth",),

    # path("ratinglist/new/", RatingListCreateView.as_view(), name="upload_rating_list",),
    path("ratinglist/<int:pk>/processor/", RatingListProcessorView.as_view(), name="rating_list_processor",),
    path("ratinglist/<slug>/", RatingListDetailView.as_view(), name="rating_list_detail",),

    # path("ratinglist/<slug>/insertplayerprofiles/", PlayerProfileCreateView.as_view(), name="create_player_profiles",),
    path("rating/<slug>/", PlayerProfileDetailView.as_view(), name="player_profile_detail",),
    path("playerprofiles/", PlayerProfileListView.as_view(), name="player_profile_list",),

    # path("federationprofile/<int:pk>/", FederationProfileDetailView.as_view(), name="federation_profile_detail",),
    # path("federationprofiles/", FederationProfileListView.as_view(), name="federation_profile_list",),
    path("federation/<str:federation_code>/", FederationDetailView.as_view(), name="federation_detail",),
    path("federations/", FederationListView.as_view(), name="federation_list",),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

