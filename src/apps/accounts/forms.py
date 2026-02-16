from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import Account


class CustomUserCreationForm(AdminUserCreationForm):

    class Meta:
        model = Account
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = (
            "email",
            "username",
        )

