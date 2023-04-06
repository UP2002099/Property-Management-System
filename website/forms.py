from django import forms
from .models import reservation

class reservationForm(forms.ModelForm):
    class Meta:
        model = reservation
        fields = ['propertyName', 'guestFirstName', 'guestLastName', 'numGuests', 'numRooms', 'bookedRoomType', 'checkInDate', 'checkOutDate', 'totalPayment']
        label = {'propertyName': 'Property', 'guestFirstName': 'First name', 'guestLastName': 'Last name', 'numGuests': 'Number of guests', 'numRooms': 'Number of rooms', 'checkInDate': 'Checkin', 'checkOutDate': 'Checkout', 'totalPayment': 'Total payment'}
        
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
        