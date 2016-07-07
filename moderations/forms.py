from django import forms

from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())


class FBGroupForm(forms.ModelForm):

    class Meta:
        model = models.FBGroup

        fields = (
            'name',
            'hate_words',
        )
