import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
# from django.http import HttpResponse
# from django.utils.encoding import escape_uri_path
# from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView


from . import forms
from . import models


# class DummyView(View):
#     def get(self, request):
#         from django.core.mail import send_mail
#
#         send_mail(
#             'Subject here',
#             'Here is the message.',
#             'from@example.com',
#             ['to@example.com'],
#             )
#         request.session['n'] = request.session.get('n', 0) + 1
#         return HttpResponse("n = {}".format(request.session['n']))
#
#
# class DummyView2(View):
#     def get(self, request):
#         assert False, request.session['visits']


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('moderations:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None and user.is_active:
            login(self.request, user)
            if self.request.GET.get('next'):
                return redirect(
                    self.request.GET['next'])  # SECURITY: check path
            return redirect('moderations:groups')

        form.add_error(None, "Invalid user name or password")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

#
# class LoggedInMixin:
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated():
#             url = reverse("login") + "?from=" + escape_uri_path(request.path)
#             return redirect(url)
#         return super().dispatch(request, *args, **kwargs)


class ListFBGroupView(LoginRequiredMixin, ListView):
    model = models.FBGroup
    paginate_by = 10
    page_title = "Home"
    # login_url = '/login/?from={}'.format(reverse_lazy("moderations:groups"))
    # redirect_field_name = 'from'

    # def get_queryset(self):
    #     return super().get_queryset().filter(group__user=self.request.user)

    def total(self):
        return 87 #self.get_queryset().aggregate(sum=Sum('amount'))['sum']

class FBGroupDetailView(LoginRequiredMixin, DetailView):
    model = models.FBGroup
    # login_url = '/login/?from=/' #todo
    # redirect_field_name = 'from'

    # def get_queryset(self):
    #     return super().get_queryset().filter(account__user=self.request.user)

    def page_title(self):
        return self.object.name

        # def get_context_data(self, **kwargs):
        #     d = super().get_context_data(**kwargs)
        #     d['title123'] = self.object.title
        #     return d


# class CreateAccountView(LoggedInMixin, CreateView):
#     page_title = _("Add New Account")
#     model = models.Expense
#     form_class = forms.AccountForm
#
#     success_url = reverse_lazy('moderations:list')
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         resp = super().form_valid(form)
#         messages.success(self.request, "Account created successfully.")
#         return resp
#
#
# class CreateExpenseView(LoggedInMixin, CreateView):
#     page_title = "Add New Expense"
#     model = models.Expense
#     fields = (
#         'account',
#         'date',
#         'amount',
#         'title',
#         'description',
#         'photo',
#     )
#
#     # success_url = reverse_lazy('moderations:list')
#
#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         # form.fields['account'].queryset = models.Account.objects.filter(
#         #     user=self.request.user)
#         form.fields['account'].queryset = form.fields[
#             'account'].queryset.filter(user=self.request.user)
#         return form
#
#     def get_initial(self):
#         d = super().get_initial()
#         d['date'] = datetime.date.today()
#         return d
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
