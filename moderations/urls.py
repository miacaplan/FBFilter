from django.conf.urls import url

from . import views

app_name = "moderations"
urlpatterns = [
    url(r'^$', views.ListFBGroupView.as_view(), name="groups"),
]
