from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from django.template.response import TemplateResponse
from django.db import models
from .models import *


#0 get today's date
def getTodayDate():
    currentDate = datetime.now().date()
    return currentDate

#1 get a week's worth of dates and the current date
def getWeekDates():
    weeklyDates = []
    for i in range(0, 8):
        if i <= 8:
            newDate = getTodayDate() + timedelta(days=i)
            weeklyDates.append(newDate)
    return weeklyDates

websites = ["Booking.com", "Traveloka"]

roomStatusColor = ["#available", "#toClean", "#unavailable"]

class bookingWebsite():
  
    def __init__(self, websiteName):
        self.websiteName = websiteName
        self.quotaConditionVar = []

    def addQuotaConditionVar(self, quota, condition):
        self.quota.append(quota)
        self.condition.append(condition)
    
    def build():
        for i in range(0, len(websites)):
            websites[i] = bookingWebsite(websites[i])
            websites[i].quotaConditionVar("roomQty" + str(i+1))
            websites[i].quotaConditionVar("conditionSelect" + str(i+1))
        return websites
        
def build():
    for i in range(0, len(websites)):
        websites[i] = bookingWebsite(websites[i])
        websites[i].quotaConditionVar("roomQty" + str(i+1))
        websites[i].quotaConditionVar("conditionSelect" + str(i+1))
    return websites

# template views
def baseTemplate(request):
    return render(request, 'base.html')

def index(request):
    #1 get this month's revenue statistics (line graph)
    labels = []
    data = []
    
    #2 get the previous quarter's revenue statistics (bar graph)
    
    #3 get today's check-ins and check-outs
    todayCheckIn = reservation.objects.filter(checkInDate=getTodayDate())
    todayCheckOut = reservation.objects.filter(checkOutDate=getTodayDate())
    numCheckIn = todayCheckIn.count()
    numCheckOut = todayCheckOut.count()
    
    context = {
        'currentDate': getTodayDate(),
        'weeklyDates': getWeekDates(),
        'todayCheckIn': todayCheckIn,
        'todayCheckOut': todayCheckOut,
        'numCheckIn': numCheckIn,
        'numCheckOut': numCheckOut
    }
    return render(request, 'index.html', context)

def walkinReservation(request):
    context = {
        'currentDate': getTodayDate(),
    }
    return render(request, 'walkinReservation.html', context)

def quotaConditions(request):
    context = {
        'websites': websites,
    }
    return render(request, 'quotaConditions.html', context)

def roomStatus(request):
    # context = {
        
    # }
    return render(request, 'roomStatus.html')

def reservations(request):
    context = {
        'currentDate': getTodayDate(),
        'weeklyDates': getWeekDates(),

    }
    return render(request, 'reservations.html', context)
