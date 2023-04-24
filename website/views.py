from django.http import HttpResponseRedirect 
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import *
from .forms import *

# get today's date
def getTodayDate():
    currentDate = datetime.now().date()
    return currentDate

def threeMonthDates():
    allReservationDates = []
    today = datetime.now().date()
    threeMonthsFromToday = today + timedelta(days=90)

    while today <= threeMonthsFromToday:
        allReservationDates.append(today)
        today += timedelta(days=1)
    return allReservationDates

# template views
def baseTemplate(request):
    return render(request, 'base.html')

def getReservations(option):
    today = getTodayDate()
    
    checkIn = []
    checkOut = []
    todayCheckIn = []
    todayCheckOut = []

    inBookingcomReservations = bookingcomReservations.objects.filter(checkInDate__gte=today)
    outBookingcomReservations = bookingcomReservations.objects.filter(checkOutDate__gte=today)
    inWalkinReservations = walkinReservations.objects.filter(checkInDate__gte=today)
    outWalkinReservations = walkinReservations.objects.filter(checkOutDate__gte=today)

    for reservation in inBookingcomReservations:
        assignedRooms = []
        getAssignedRooms = AssignedRoom.objects.filter(reservation=reservation)
        assignedRooms = list(getAssignedRooms)

        checkIn.append((reservation, assignedRooms))

        if reservation.checkInDate == today:
            todayCheckIn.append((reservation, assignedRooms))
            
    for reservation in outBookingcomReservations:
        assignedRooms = []
        getAssignedRooms = AssignedRoom.objects.filter(reservation=reservation)
        assignedRooms = list(getAssignedRooms)

        checkOut.append((reservation, assignedRooms))

        if reservation.checkOutDate == today:
            todayCheckOut.append((reservation, assignedRooms))
            
    for reservation in inWalkinReservations:
        assignedRooms = []
        getAssignedRooms = [reservation.assignedRoom]
        assignedRooms = list(getAssignedRooms)
        
        checkIn.append((reservation, assignedRooms))

        if reservation.checkOutDate == today:
            todayCheckIn.append((reservation, assignedRooms))
    
    for reservation in outWalkinReservations:
        assignedRooms = []
        getAssignedRooms = [reservation.assignedRoom]
        assignedRooms = list(getAssignedRooms)
        
        checkOut.append((reservation, assignedRooms))

        if reservation.checkOutDate == today:
            todayCheckOut.append((reservation, assignedRooms))

    if option == 'checkIn':
        return checkIn
    elif option == 'checkOut':
        return checkOut
    elif option == 'todayCheckIn':
        return todayCheckIn
    elif option == 'todayCheckOut':
        return todayCheckOut

# note: NO WALKIN RESERVATION AS WALKINS REQUIRE AN AVAILABLE ROOM TO BE ABLE TO MAKE A RESERVATION!!!!!!!! 
def availableRooms(option):
    today = getTodayDate()

    # get all reservations that have checkindate greater or equal to today
    checkInReservations = bookingcomReservations.objects.filter(checkInDate__gte=today)
    
    # get all reservations - for checkoutdate (very long stays)
    allReservations = bookingcomReservations.objects.all()
    
    roomTypePerDay = {}
    
    # empty queryset
    noAssignedRooms = bookingcomReservations.objects.none()

    for reservation in checkInReservations:
        # reservations that have assigned rooms will be excluded as roomStatus will be 'unavailable'
        assignedRooms = AssignedRoom.objects.filter(reservation=reservation)
        if not assignedRooms:
            noAssignedRooms |= bookingcomReservations.objects.filter(pk=reservation.pk) # add to the queryset

    # Loop through each day of the week
    for i in range(8):
        day = today + timedelta(days=i)
        print(day)
        checkInToday = noAssignedRooms.filter(checkInDate=day)
        checkOutToday = allReservations.filter(checkOutDate=day)

        # For the first day, count the number of reservations and return an output that minuses 
        # the total number of available rooms with the number of reservations
        if i == 0:
            currentSingle = buildingRoom.objects.filter(roomType='Single Bed Room', roomStatus='available').count()
            currentTwin = buildingRoom.objects.filter(roomType='Twin Bed Room', roomStatus='available').count()
            
            # checkout = guest return rooms
            for r in checkOutToday:
                currentSingle += r.numSingle
                currentTwin += r.numTwin
            
            # checkin = guest take rooms
            for r in checkInToday:
                currentSingle -= r.numSingle
                currentTwin -= r.numTwin

            # append to dictionary
            roomTypePerDay[day] = {
                'single': currentSingle,
                'twin': currentTwin,
                'total': currentSingle + currentTwin
            }
            
            currentTotal = currentSingle + currentTwin
            
        else:
            # If a reservation has the checkOutDate equal to today increase room count accordingly
            for r in allReservations:
                if r.checkOutDate == day:
                    currentSingle += r.numSingle
                    currentTwin += r.numTwin
            
            # If a reservation has their checkInDate equal to today, decrease room count accordingly
            for r in allReservations:
                if r.checkInDate == day:
                    currentSingle -= r.numSingle
                    currentTwin -= r.numTwin

            # Store the number of rooms per type for today
            roomTypePerDay[day] = {
                'single': currentSingle,
                'twin': currentTwin,
                'total': currentSingle + currentTwin
            }
    
    if option == 'weekly':
        return roomTypePerDay
    elif option == 'currentTotal':
        return currentTotal

def loadtester(request):
    return render(request, 'loaderio-bc96bfa09c42c1a4d4c6e65bb3cf5ffe.html')

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
        'todayCheckIn': getReservations('todayCheckIn'),
        'todayCheckOut': getReservations('todayCheckOut'),
        'availableRooms': availableRooms('weekly'),
        'currentTotal': availableRooms('currentTotal'),
        'numCheckIn': numCheckIn,
        'numCheckOut': numCheckOut,
    }
    return render(request, 'index.html', context)

def buildingStatus(option):
    paraisoFloorRooms = {}
    toClean = []
    paraisoRoomStatus = {'available': 0, 'unavailable': 0, 'cleaning': 0, 'apartment': 0}
    roomTypeCount = {'single': 0, 'twin': 0}
    roomNumbers = {'single': [], 'twin': []}

    for room in buildingRoom.objects.all().values('roomNum', 'roomFloor', 'roomStatus', 'roomType'):
        floorNum = room['roomFloor']
        if floorNum not in paraisoFloorRooms:
            paraisoFloorRooms[floorNum] = {'rooms': [], 'available': 0, 'unavailable': 0, 'cleaning': 0, 'apartment': 0, 'roomTypeCount': {}}
        
        # Counts only the number of room types that are available and appends the room number
        if room['roomType'] == 'Single Bed Room':
            if room['roomStatus'] == 'available':
                roomTypeCount['single'] += 1
                roomNumbers['single'].append(room['roomNum'])
        elif room['roomType'] == 'Twin Bed Room':
            if room['roomStatus'] == 'available':
                roomTypeCount['twin'] += 1
                roomNumbers['twin'].append(room['roomNum'])
        
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
        'paraisoRoomTypeCount': buildingStatus('roomTypeCount'),
        'toClean': buildingStatus('toClean'),
        'form': form,
    }
    return render(request, 'roomStatus.html', context)

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
            roomData = {
                'room_num': room.roomNum,
                'room_price': roomType.roomPrice
            }
            roomTypeData['rooms'].append(roomData)
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

def allReservations(request):
    
    context = {
        'currentDate': getTodayDate(),
        'threeMonthDates': threeMonthDates(),
        'threeMonthIn':getReservations('checkIn'),
        'threeMonthOut':getReservations('checkOut'),
    }
    return render(request, 'allReservations.html', context)