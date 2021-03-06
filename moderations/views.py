import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy, reverse
# from django.http import HttpResponse
# from django.utils.encoding import escape_uri_path
# from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView

from . import forms
from . import models
from FB import fb_utils


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


# class LoginView(FormView):
#     form_class = forms.LoginForm
#     template_name = "login.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated():
#             return redirect('moderations:list')
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         user = authenticate(username=form.cleaned_data['username'],
#                             password=form.cleaned_data['password'])
#
#         if user is not None and user.is_active:
#             login(self.request, user)
#             if self.request.GET.get('next'):
#                 return redirect(
#                     self.request.GET['next'])  # SECURITY: check path
#             return redirect('moderations:groups')
#
#         form.add_error(None, "Invalid user name or password")
#         return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("social:begin", kwargs={"backend": "facebook"}))


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

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(moderators__exact=self.request.user.moderator.id) | Q(administrator=self.request.user.moderator.id)
        )

    def total(self):
        return 87  # self.get_queryset().aggregate(sum=Sum('amount'))['sum']

class ListPostmentView(LoginRequiredMixin, ListView):
    model = models.Postment
    paginate_by = 10
    page_title = "Posts & Comments to Moderate"

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(group__moderators__exact=self.request.user.moderator.id) | Q(group__administrator=self.request.user.moderator.id)
        )

class FBGroupDetailView(LoginRequiredMixin, DetailView):
    model = models.FBGroup
    template_name = "moderations/postment_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(moderators__exact=self.request.user.moderator.id) | Q(administrator=self.request.user.moderator.id)
        )

    def page_title(self):
        return self.object.name

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        paginator = Paginator(self.object.postments.all(), 1)
        page_num = self.request.GET.get('page', 1)
        d['page_obj'] = paginator.page(page_num)
        d['object_list'] = d['page_obj'].object_list
        return d

class FBGroupMixin:
    template_name = "moderations/fbgroup_form.html"

    form_class = forms.FBGroupForm
    success_url = reverse_lazy('moderations:home')

    def get_initial(self):
        return super().get_initial()

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d[
            'moderator_list'] = models.Moderator.objects.all()  # [{'label': m.user.username, 'value': m.user.social_auth.get(provider='facebook').uid} for m in models.Moderator.objects.all()]
        return d

    def form_valid(self, form):
        return super().form_valid(form)

class CreateFBGroupView(LoginRequiredMixin, FBGroupMixin, CreateView):

    def title(self):
        return "New Group Registration"

    def form_valid(self, form):
        fb_user = self.request.user.social_auth.get(provider='facebook')
        if not fb_utils.is_group_admin(self.request.POST['group_id'], fb_user.uid,
                                       fb_user.extra_data['access_token']):
            form.add_error(None, "Only groups administered by you may be registered")
            return self.form_invalid(form)
        try:
            form.instance.administrator = self.request.user.moderator
            form.instance.fb_group_id = self.request.POST['group_id']
            resp = super().form_valid(form)
            # form.instance.moderators.add(self.request.user.moderator)
            messages.success(self.request, 'Succefully registered: ' + form.instance.name)
            return resp
        except IntegrityError:
            form.add_error(None, "Group {} already exists".format(form.instance.name))
            return self.form_invalid(form)
        except Exception as e:
            form.add_error(None,
                           "Error occured when attempting to register group {}:\n{}".format(form.instance.name,
                                                                                            e.args))
            return self.form_invalid(form)

class UpdateFBGroupView(LoginRequiredMixin, FBGroupMixin, UpdateView):
    model = models.FBGroup

    def get_queryset(self):
        return super().get_queryset().filter(administrator=self.request.user.moderator.id)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].disabled = True
        return form

    def title(self):
        return self.object.name

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, 'Succefully updated group: ' + form.instance.name)
        return resp

