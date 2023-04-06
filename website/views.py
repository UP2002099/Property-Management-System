from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.template.response import TemplateResponse
from django.db.models import Count
from django.db import models
from .models import *
from .forms import reservationForm

# get today's date
def getTodayDate():
    currentDate = datetime.now().date()
    return currentDate

# get a week's worth of dates and the current date
def getWeekDates():
    weeklyDates = []
    for i in range(0, 8):
        if i <= 8:
            newDate = getTodayDate() + timedelta(days=i)
            weeklyDates.append(newDate)
    return weeklyDates

def threeMonthDates():
    threeMonthsOfDates = []
    today = datetime.now().date()
    threeMonthsFromToday = today + timedelta(days=90)

    while today <= threeMonthsFromToday:
        threeMonthsOfDates.append(today)
        today += timedelta(days=1)
    return threeMonthsOfDates

websites = ['Booking.com', 'Traveloka']

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

def getFloorInfo(option):
    paraisoFloorRooms = {}
    toClean = []
    paraisoRoomStatus = {'available': 0, 'unavailable': 0, 'cleaning': 0}
    paraisoRooms = buildingRoom.objects.all().values('roomNum', 'roomFloor', 'roomStatus')
    for room in paraisoRooms:
        floorNum = room['roomFloor']
        if floorNum not in paraisoFloorRooms:
            paraisoFloorRooms[floorNum] = {'rooms': [], 'available': 0, 'unavailable': 0, 'cleaning': 0}
        paraisoFloorRooms[floorNum]['rooms'].append(room)
        if room['roomStatus'] == 'available':
            paraisoFloorRooms[floorNum]['available'] += 1
            paraisoRoomStatus['available'] += 1
        elif room['roomStatus'] == 'unavailable':
            paraisoFloorRooms[floorNum]['unavailable'] += 1
            paraisoRoomStatus['unavailable'] += 1
        elif room['roomStatus'] == 'cleaning':
            paraisoFloorRooms[floorNum]['cleaning'] += 1
            paraisoRoomStatus['cleaning'] += 1
            toClean.append(room)
    
    if option == 'floorRoom':
        return paraisoFloorRooms
    elif option == 'roomStatus':
        return paraisoRoomStatus
    elif option == 'toClean':
        return toClean
    

def walkinReservation(request):
    
    form = reservationForm()
    if request.method == 'POST':
        form = reservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/website')
    
    context = {
        'currentDate': getTodayDate(),
        'form': form,
        'paraisoRoomStatus': getFloorInfo('roomStatus'),
    }
    return render(request, 'walkinReservation.html', context)

def roomStatus(request):
    context = {
        'paraisoFloorRooms': getFloorInfo('floorRoom'),
        'paraisoRoomStatus': getFloorInfo('roomStatus'),
        'toClean': getFloorInfo('toClean'),
    }
    return render(request, 'roomStatus.html', context)

def quotaConditions(request):
    
    hotelRooms = len(buildingRoom.objects.filter(roomSection='Hotel'))
    
    context = {
        'websites': websites,
        'hotelRooms': hotelRooms,
    }
    return render(request, 'quotaConditions.html', context)

def getReservations():
    reservationsList = []
    today = datetime.now().date()
    threeMonthsFromToday = today + timedelta(days=90)

    for i in range(0, 9):
        reservationDate = today + timedelta(days=i)
        initialDate = reservationDate
        threeMonthsFromToday = initialDate + timedelta(days=1)
        getReservations = reservation.objects.filter(checkInDate=initialDate).filter(checkInDate=threeMonthsFromToday)
        reservationsList.extend(list(getReservations))
    return reservationsList

def allReservations(request):
    
    context = {
        'currentDate': getTodayDate(),
        'weeklyDates': getWeekDates(),
        'threeMonthDates': threeMonthDates(),
        'threeMonthsReservations':getReservations(),
    }
    return render(request, 'allReservations.html', context)