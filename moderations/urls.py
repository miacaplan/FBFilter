from django.conf.urls import url

from . import views

app_name = "moderations"
urlpatterns = [
    url(r'^$', views.ListPostmentView.as_view(), name="home"),
    url(r'^group/$', views.ListFBGroupView.as_view(), name="groups"),
    url(r'^group/(?P<pk>\d+)/$', views.FBGroupDetailView.as_view(), name="group"),
]
