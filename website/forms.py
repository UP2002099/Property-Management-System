from django import forms
from .models import *

class reservationForm(forms.ModelForm):
    class Meta:
        model = reservation
        fields = ['propertyName', 'guestFirstName', 'guestLastName', 'numGuests', 'numRooms', 'bookedRoomType', 'checkInDate', 'checkOutDate', 'totalPayment']
        labels = {'propertyName': 'Property', 'guestFirstName': 'First Name', 'guestLastName': 'Last Name', 'numGuests': 'Number of Guests', 'numRooms': 'Number of Rooms', 'bookedRoomType': 'Room Type' ,'checkInDate': 'Check-In Date', 'checkOutDate': 'Check-Out Date', 'totalPayment': 'Total Payment'}
        
        widgets = {
            'propertyName': forms.Select(attrs={'class': 'form-control'}),
            'guestFirstName': forms.TextInput(attrs={'class': 'form-control'}),
            'guestLastName': forms.TextInput(attrs={'class': 'form-control'}),
            'numGuests': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'numRooms': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'bookedRoomType': forms.Select(attrs={'class': 'form-control'}),
            'checkInDate': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'checkOutDate': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'totalPayment': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

class cleaningForm(forms.Form):
    roomNum = forms.ModelMultipleChoiceField(
        queryset=buildingRoom.objects.filter(roomStatus='cleaning'),
        widget=forms.CheckboxSelectMultiple,
        label=''
    )
        
class RoomConditionForm(forms.ModelForm):
    class Meta:
        model = buildingRoom
        fields = ['listedWebsites', 'roomType', 'roomPrice', 'roomStatus']

    listedWebsites = forms.ModelChoiceField(queryset=bookingWebsite.objects.all())
    roomType = forms.ModelChoiceField(queryset=roomPrices.objects.all())
    roomPrice = forms.DecimalField(max_digits=8, decimal_places=2)
    roomStatus = forms.ChoiceField(choices=buildingRoom.STATUS, widget=forms.Select(attrs={'class': 'form-control'}))