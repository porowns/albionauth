from django.conf.urls import url, include
from django.contrib import admin
import views
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^character/add/$', views.character_add, name='character_add'),
    url(r'^character/remove/$', views.character_remove, name='character_remove'),
    url(r'^character/update/$', views.character_update, name='character_update'),
    url(r'^character/list/$', views.character_list, name='character_list'),
    url(r'^craft/update/$', views.craft_update, name='craft_update'),
    url(r'^craft/list/$', views.craft_list, name='craft_list')
]
