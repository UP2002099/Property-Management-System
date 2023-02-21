from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('navbar/', views.navbar, name='navbar'),
    path('walkinReservation/', views.walkinReservation, name='walkinReservation'),
    path('quotaConditions/', views.quotaConditions, name='quotaConditions'),

]