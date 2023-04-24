from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('baseTemplate/', views.baseTemplate, name='baseTemplate'),
    path('walkinReservation/', views.walkinReservation, name='walkinReservation'),
    path('quotaConditions/', views.quotaConditions, name='quotaConditions'),
    path('roomStatus/', views.roomStatus, name='roomStatus'),
    path('reservations/', views.allReservations, name='allReservations'),
    path('editQuotaConditions/', views.editQuotaConditions, name='editQuotaConditions'),
    path('loadSelectRoom/', views.loadSelectRoom, name='loadSelectRoom'),
    path('loadSelectRoomPrice/', views.loadSelectRoomPrice, name='loadSelectRoomPrice'),
    path('loaderio-bc96bfa09c42c1a4d4c6e65bb3cf5ffe', views.loadtester, name='loadtester'),
]