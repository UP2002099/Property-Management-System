from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('baseTemplate/', views.baseTemplate, name='baseTemplate'),
    path('walkinReservation/', views.walkinReservation, name='walkinReservation'),
    path('quotaConditions/', views.quotaConditions, name='quotaConditions'),
    path('roomStatus/', views.roomStatus, name='roomStatus'),
    path('reservations/', views.allReservations, name='allReservations'),

]