"""
This is the forms module for the "ratinglists" Django app.
"""


from django import forms

from .models import RatingList
from .models import Post


class PostForm(forms.ModelForm):

    uploaded_file = forms.FileField(label = False)

    class Meta:

        model = Post

        fields = ["uploaded_file",]


class RatingListForm(forms.ModelForm):

    uploaded_file = forms.FileField(label = False)

    class Meta:

        model = RatingList

        fields = ["uploaded_file",]

