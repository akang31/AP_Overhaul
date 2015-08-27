from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'index', views.index, name='index'),
    url(r'table', views.table, name='table'),
    url(r'itemPage/([0-9]+)', views.itemPage, name='itemPage')
]
