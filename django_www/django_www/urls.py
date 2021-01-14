from django.conf import settings
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index),

    # APIs
    re_path(r'^api/create', views.create),
    re_path(r'^api/parse', views.show_url),

    re_path(r'([a-zA-Z0-9]{5})', views.redirect_shorten_url),
]
