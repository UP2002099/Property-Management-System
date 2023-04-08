from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.template.response import TemplateResponse
from django.db.models import Count
from django.db import models
from .models import *
from .forms import *

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

# template views
def baseTemplate(request):
    return render(request, 'base.html')

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

# WEBSITE TEMPLATE VIEWS

def index(request):
    #1 get this month's revenue statistics (line graph)
    labels = []
    data = []
    
    #2 get the previous quarter's revenue statistics (bar graph)
    
    #3 get today's check-ins and check-outs
    todayCheckIn = reservationModel.objects.filter(checkInDate=getTodayDate())
    todayCheckOut = reservationModel.objects.filter(checkOutDate=getTodayDate())
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
    if request.method == 'POST':
        form = cleaningForm(request.POST)
        if form.is_valid():
            roomNum = form.cleaned_data['roomNum']
            roomNum.update(roomStatus='available')
    else:
        form = cleaningForm()
    
    context = {
        'paraisoFloorRooms': getFloorInfo('floorRoom'),
        'paraisoRoomStatus': getFloorInfo('roomStatus'),
        'toClean': getFloorInfo('toClean'),
        'form': form,
    }
    return render(request, 'roomStatus.html', context)

def quotaConditions(request):
    
    totalHotelRooms = len(buildingRoom.objects.filter(roomSection='Hotel'))
        
    websites = bookingWebsite.objects.all()
    websiteData = []
    for website in websites:
        roomData = roomPrices.objects.filter(listedWebsite=website)
        websiteData.append({'website': website, 'roomPrices': roomData})
    
    context = {
        'totalHotelRooms': totalHotelRooms,
        'websiteData': websiteData,
    }
    return render(request, 'quotaConditions.html', context)

def editQuotaConditions(request):
    
    totalHotelRooms = len(buildingRoom.objects.filter(roomSection='Hotel'))
    
    data = []
    roomPricing = roomPrices.objects.all()
    for roomType in roomPricing:
        rooms = buildingRoom.objects.filter(roomType=roomType)
        roomTypeData = {
            'roomType': roomType.roomType,
            'rooms': []
        }
        for room in rooms:
            room_data = {
                'room_num': room.roomNum,
                'room_price': roomType.roomPrice
            }
            roomTypeData['rooms'].append(room_data)
        data.append(roomTypeData)

    if request.method == 'POST':
        form = RoomConditionForm(request.POST)
        if form.is_valid():
            roomType = form.cleaned_data['roomType']
            roomPrice = form.cleaned_data['roomPrice']

            buildingRoom.objects.filter(roomType=roomType).update(roomPrice=roomPrice)

    else:
        form = RoomConditionForm()
        
    context = {
        'data': data,
        'form': form,
        'totalHotelRooms': totalHotelRooms,
    }
    return render(request, 'editQuotaConditions.html', context)

# allReservations TEMPLATE
def threeMonthDates():
    threeMonthsOfDates = []
    today = datetime.now().date()
    threeMonthsFromToday = today + timedelta(days=90)

    while today <= threeMonthsFromToday:
        threeMonthsOfDates.append(today)
        today += timedelta(days=1)
    return threeMonthsOfDates

def getReservations():
    reservationsList = []
    threeMonthDatesList = threeMonthDates()
    
    for reservations_date in threeMonthDatesList:
        start_date = reservations_date
        finalDate = start_date + timedelta(days=1)
        reservation_queryset = reservationModel.objects.filter(checkInDate__gte=start_date, checkInDate__lt=finalDate)
        reservationsList.extend(list(reservation_queryset))
    return reservationsList

def allReservations(request):
    
    context = {
        'currentDate': getTodayDate(),
        'weeklyDates': getWeekDates(),
        'threeMonthDates': threeMonthDates(),
        'threeMonthsReservations':getReservations(),
    }
    return render(request, 'allReservations.html', context)