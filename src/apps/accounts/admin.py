from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Account


class AdminAccount(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Account
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_active",
    ]


admin.site.register(Account, AdminAccount)

