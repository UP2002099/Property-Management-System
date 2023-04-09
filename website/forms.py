from django import forms
from .models import *

class walkinReservationForm(forms.ModelForm):
    class Meta:
        # Stops form from loading all 'assignedRoom' fields
        assignedRoom = forms.ModelChoiceField(queryset=buildingRoom.objects.none(), label='Select a room')
        model = walkinReservationModel
        fields = [
            'propertyName', 'guestFirstName', 'guestLastName', 
            'numGuests', 'numRooms', 'roomType',
            'assignedRoom', 'checkInDate', 'checkOutDate', 'totalPayment',
        ]
        labels = {
            'propertyName': 'Property', 'guestFirstName': 'First Name',
            'guestLastName': 'Last Name', 'numGuests': 'Number of Guests',
            'numRooms': 'Number of Rooms', 'roomType': 'Select room type', 
            'assignedRoom': 'Select a room', 'checkInDate': 'Check-In Date', 
            'checkOutDate': 'Check-Out Date', 'totalPayment': 'Total Payment', 
        }

        widgets = {
            'propertyName': forms.Select(attrs={'class': 'form-control'}),
            'guestFirstName': forms.TextInput(attrs={'class': 'form-control'}),
            'guestLastName': forms.TextInput(attrs={'class': 'form-control'}),
            'numGuests': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'numRooms': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'roomType': forms.Select(attrs={'class': 'form-control', 'id':'roomType'}),
            'assignedRoom': forms.Select(attrs={'class': 'form-control'}),
            'checkInDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'checkOutDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'totalPayment': forms.NumberInput(attrs={'class': 'form-control', 'id':'paymentAmount', 'readonly': 'readonly'}),
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
    roomType = forms.ModelChoiceField(queryset=priceForRoomType.objects.all())
    roomPrice = forms.DecimalField(max_digits=8, decimal_places=2)
    roomStatus = forms.ChoiceField(choices=buildingRoom.STATUS, widget=forms.Select(attrs={'class': 'form-control'}))