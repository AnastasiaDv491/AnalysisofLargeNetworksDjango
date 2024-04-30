from django import forms

from .models import document


class PostForm(forms.ModelForm):

    class Meta:
        model = document
        fields = (
            "doc_id",
            "about",
        )
