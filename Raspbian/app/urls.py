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
]