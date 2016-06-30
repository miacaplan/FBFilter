from django import forms

# from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())


# class AccountForm(forms.ModelForm):
#     class Meta:
#         model = models.Account
#         exclude = (
#             'user',
#         )


# class ExpenseForm(forms.ModelForm):
#     class Meta:
#         model = models.Expense
#         exclude = (
#         )
