from django import forms

from .models import Review

class CreateReviewForm(forms.Form):
    comments = forms.CharField(label="",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Comment your review..."
            }
        )
    )
    