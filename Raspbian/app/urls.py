from django.conf.urls import url
from django.urls import path
from app import views

urlpatterns = [
    path('login/',views.login),
    path('logout/',views.logout),
    path('',views.index),
    path('look/',views.look),
    path('history/',views.history),
    path('face/',views.face),
    path('take_a_photo/',views.take_a_photo),
    path('face_compare/',views.face_compare),
    # url(r'^login$', views.login),
    # url(r'^logout$', views.logout),
    # url(r'^$', views.index),
    # url(r'^look$', views.look),
    # url(r'^control$', views.control),
    # url(r'^face$', views.face),
    # url(r'^take_a_photo$',views.take_a_photo),
    # url(r'^face_compare$',views.face_compare),
]