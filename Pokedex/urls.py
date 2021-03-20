from django.conf.urls import include, url
from . import views
# 用來串接callback主程式
urlpatterns = [
    url('create/', views.create),
    url('update/', views.update),
    url('retrieve/', views.retrieve),
    url('retrieveByType/', views.retrieveByType),
    url('addEvolution/', views.addEvolution),
    url('deleteEvolution/', views.deleteEvolution)
]