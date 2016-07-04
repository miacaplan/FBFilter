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
        )
    # start = forms.DateTimeField(label='starts at', widget=DateTimeWidget(bootstrap_version=3, attrs={'data-readonly': 'false'}))
    # end = forms.DateTimeField(label='ends at', widget=DateTimeWidget(bootstrap_version=3, attrs={'data-readonly': 'false'}))