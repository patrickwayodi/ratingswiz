from django.contrib import admin

from .models import RatingList, FederationList, FederationProfile, PlayerProfile, Post


admin.site.register(RatingList)
admin.site.register(FederationList)
admin.site.register(FederationProfile)
admin.site.register(PlayerProfile)
admin.site.register(Post)

