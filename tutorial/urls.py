from django.conf.urls import include, url
from django.contrib import admin
from polls.views import *
urlpatterns = [
    url(r'^$',main_page),
    url(r'^polls/', include('polls.urls',namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
    ]