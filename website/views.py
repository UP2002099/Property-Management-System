from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta

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

def index(request):
    #2 get this month's revenue statistics (line graph)
    labels = []
    data = []
    
    #3 get the previous quarter's revenue statistics (bar graph)
    
    context = {
        'currentDate': getTodayDate(),
        'weeklyDates': getWeekDates(),
    }
    return render(request, 'index.html', context)

def walkinReservation(request):
    context = {
        'currentDate': getTodayDate(),
    }
    return render(request, 'walkinReservation.html', context)

def navbar(request):
    return render(request, 'navbar.html')
