from django.conf.urls import url
from django.urls import path
from app import cp_views as views

urlpatterns = [
    path('login/',views.login),
    path('logout/',views.logout),
    path('',views.index),
    path('look/',views.look),
    path('control/',views.control),
    path('face/',views.face),
    # url(r'^login$', views.login),
    # url(r'^logout$', views.logout),
    # url(r'^$', views.index),
    # url(r'^look$', views.look),
    # url(r'^control$', views.control),
    # url(r'^face$', views.face),
    # url(r'^take_a_photo$',views.take_a_photo),
    # url(r'^face_compare$',views.face_compare),
]