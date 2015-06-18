from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^main/$', views.main_page, name='main'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/run/$', views.run, name='run'),
#    url(r'^(?P<question_id>[0-9]+)/go/$', views.go, name='go'),
#    url(r'^login/$','django.contrib.auth.views.login'),
    url(r'^login/$',views.login_page),
    url(r'^logout/$',views.logout_page),
    url(r'^register/$',views.register_page),

]