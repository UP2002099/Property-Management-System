from django.http import HttpResponseRedirect 
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import *
from .forms import *

# import external reservations into django
def bookingcomCsv(request):
    csv = open(r'C:\Users\pound\OneDrive\propertyManagementSystem\cleanedScraper11', 'r')

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

def getReservations(option):
    today = getTodayDate()
    allReservationDates = threeMonthDates()
    
    allReservations = []
    todayCheckIn = []
    todayCheckOut = []
    
    for date in allReservationDates:
        externalBooking = bookingcomReservations.objects.filter(checkInDate__gte=date, checkInDate__lt=date+timedelta(days=1))
        walkinBooking = walkinReservations.objects.filter(checkInDate__gte=date, checkInDate__lt=date+timedelta(days=1))
        allReservations.extend(list(externalBooking) + list(walkinBooking))
        
        if date == today:
            todayCheckIn.extend(list(externalBooking) + list(walkinBooking))
            todayCheckOut.extend(list(bookingcomReservations.objects.filter(checkOutDate=date)) + list(walkinReservations.objects.filter(checkOutDate=date)))
        
    if option == 'allReservations':
        return allReservations
    elif option == 'todayCheckIn':
        return todayCheckIn
    elif option == 'todayCheckOut':
        return todayCheckOut

# WEBSITE TEMPLATE VIEWS

def index(request):
    #1 get this month's revenue statistics (line graph)
    labels = []
    data = []
    
    #2 get the previous quarter's revenue statistics (bar graph)
    
    #3 get today's check-ins and check-outs
    numCheckIn = len(getReservations('todayCheckIn'))
    numCheckOut = len(getReservations('todayCheckOut'))
    
    context = {
        'currentDate': getTodayDate(),
        'weeklyDates': getWeekDates(),
        'todayCheckIn': getReservations('todayCheckIn'),
        'todayCheckOut': getReservations('todayCheckOut'),
        'numCheckIn': numCheckIn,
        'numCheckOut': numCheckOut,
    }
    return render(request, 'index.html', context)

def buildingStatus(option):
    paraisoFloorRooms = {}
    toClean = []
    paraisoRoomStatus = {'available': 0, 'unavailable': 0, 'cleaning': 0, 'apartment': 0}
    roomTypeCount = {'Single Bed Room': 0, 'Twin Bed Room': 0}
    roomNumbers = {'Single Bed Room': [], 'Twin Bed Room': []}

    for room in buildingRoom.objects.all().values('roomNum', 'roomFloor', 'roomStatus', 'roomType'):
        floorNum = room['roomFloor']
        if floorNum not in paraisoFloorRooms:
            paraisoFloorRooms[floorNum] = {'rooms': [], 'available': 0, 'unavailable': 0, 'cleaning': 0, 'apartment': 0, 'roomTypeCount': {}}
        
        # Counts only the number of room types that are available and appends the room number
        if room['roomType'] == 'Single Bed Room':
            if room['roomStatus'] == 'available':
                roomTypeCount['Single Bed Room'] += 1
                roomNumbers['Single Bed Room'].append(room['roomNum'])
        elif room['roomType'] == 'Twin Bed Room':
            if room['roomStatus'] == 'available':
                roomTypeCount['Twin Bed Room'] += 1
                roomNumbers['Twin Bed Room'].append(room['roomNum'])
        
        # Iterates through floors of the building and collects and their information
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
        elif room['roomStatus'] == 'apartment':
            paraisoFloorRooms[floorNum]['apartment'] += 1
            paraisoRoomStatus['apartment'] += 1
    
    if option == 'floorRoom':
        return paraisoFloorRooms
    elif option == 'roomStatus':
        return paraisoRoomStatus
    elif option == 'toClean':
        return toClean
    elif option == 'roomTypeCount':
        return roomTypeCount
    elif option == 'roomNumbers':
        return roomNumbers

# AJAX QUERY SHOW ROOM TYPE
def loadSelectRoom(request):
    selectedRoomType = request.GET.get('selectedRoomType')
    availableRooms = buildingRoom.objects.filter(roomType=selectedRoomType, roomStatus='available')
    
    context = {
        'rooms': availableRooms
    }
    
    return render(request, 'loadSelectRoom.html', context)

# AJAX QUERY SHOW ROOM PRICE FOR SELECTED ROOM TYPE
def loadSelectRoomPrice(request):
    selectedRoomType = request.GET.get('selectedRoomType')
    roomPrice = priceForRoomType.objects.get(roomType=selectedRoomType).roomPrice
    
    context = {
        'prices': str(roomPrice)
    }
    
    return render(request, 'loadSelectRoomPrice.html', context)

def walkinReservation(request):
    form = walkinReservationForm()
    
    if request.method == 'POST':
        form = walkinReservationForm(request.POST)
        if form.is_valid():
            # Stop save function to compute reservation logic
            reservation = form.save(commit=False)
            
            # get POST data via name - loadSelectRoom.html lacks a name value, 
            # but it has taken the name value from the 'field' list in form.py!
            # so don't get confused when looking back
            selectedFormRoom = request.POST.get('assignedRoom')
            selectedFormRoomTypePrice = request.POST.get('totalPayment')
            
            # make sure chosen room is now set as unavailable
            databaseRoom = buildingRoom.objects.get(roomNum=selectedFormRoom)
            databaseRoom.roomStatus = 'unavailable'
            databaseRoom.save()
            
            # make changes to the reservation form
            reservation.assignedRoom = databaseRoom
            reservation.totalPayment = selectedFormRoomTypePrice
            reservation.save()
            return HttpResponseRedirect("/website/")

    context = {
        'currentDate': getTodayDate(),
        'form': form,
        'paraisoRoomStatus': buildingStatus('roomStatus'),
        'paraisoRoomTypeCount': buildingStatus('roomTypeCount'),
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
        'paraisoFloorRooms': buildingStatus('floorRoom'),
        'paraisoRoomStatus': buildingStatus('roomStatus'),
        'toClean': buildingStatus('toClean'),
        'form': form,
    }
    return render(request, 'roomStatus.html', context)

def quotaConditions(request):
    
    totalHotelRooms = len(buildingRoom.objects.filter(roomSection='Hotel'))
        
    websites = bookingWebsite.objects.all()
    websiteData = []
    for website in websites:
        roomData = priceForRoomType.objects.filter(listedWebsite=website)
        websiteData.append({'website': website, 'roomPrices': roomData})
    
    context = {
        'totalHotelRooms': totalHotelRooms,
        'websiteData': websiteData,
    }
    return render(request, 'quotaConditions.html', context)

def editQuotaConditions(request):
    
    totalHotelRooms = len(buildingRoom.objects.filter(roomSection='Hotel'))
    
    data = []
    roomPricing = priceForRoomType.objects.all()
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
        form = roomConditionForm(request.POST)
        if form.is_valid():
            roomType = form.cleaned_data['roomType']
            roomPrice = form.cleaned_data['roomPrice']

            buildingRoom.objects.filter(roomType=roomType).update(roomPrice=roomPrice)

    else:
        form = roomConditionForm()
        
    context = {
        'data': data,
        'form': form,
        'totalHotelRooms': totalHotelRooms,
    }
    return render(request, 'editQuotaConditions.html', context)

# allReservations TEMPLATE
def threeMonthDates():
    allReservationDates = []
    today = datetime.now().date()
    threeMonthsFromToday = today + timedelta(days=90)

    while today <= threeMonthsFromToday:
        allReservationDates.append(today)
        today += timedelta(days=1)
    return allReservationDates

def allReservations(request):
    
    context = {
        'currentDate': getTodayDate(),
        'weeklyDates': getWeekDates(),
        'threeMonthDates': threeMonthDates(),
        'threeMonthsReservations':getReservations('allReservations'),
    }
    return render(request, 'allReservations.html', context)