import csv
from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from website.models import bookingcomReservations, bookingWebsite, buildingRoom
from decimal import Decimal
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(r'C:\Users\pound\OneDrive\propertyManagementSystem\apr12_apr19.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rowHeader = next(reader)
            
            # rename original header rows
            rowHeader[0] = 'guestName'
            rowHeader[1] = 'numGuests'
            rowHeader[2] = 'checkInDate'
            rowHeader[3] = 'checkOutDate'
            rowHeader[4] = 'resRoomType'
            rowHeader[5] = 'reservationStatus'
            rowHeader[6] = 'totalPayment'
            rowHeader[7] = 'commission'
            rowHeader[8] = 'extReservationId'
            rowHeader[9] = 'smartFlex'

            for row in reader:
                # THB 0 means no payment (etc guest cancelled) = remove from list
                if 'THB 0' not in row:
                    resRoomType = row[4]
                    numGuests = row[1]
                    totalPayment = row[6]
                    commission = row[7]
                    numSingle = 0
                    numTwin = 0
                    
                    # take only the number of guests as numGuests format = x guests
                    row[1] = int(numGuests.split()[0])
                    
                    # format to decimalField - THB is always before the decimalField
                    row[6] = Decimal(totalPayment.replace('THB ', '').replace(',',''))
                    row[7] = Decimal(commission.replace('THB ', '').replace(',',''))
                    
                    # double ifs as multiple rooms can be composed of multiple room types
                    if 'Single Bed Room' in resRoomType:
                        if 'x' not in resRoomType and ',' not in resRoomType: # [Single Bed Room]: numSingle = 1
                            numSingle = 1
                        elif 'x' in resRoomType and ',' not in resRoomType: # [2 x Single Bed Room]: numSingle = 2
                            numSingle = int(resRoomType.split()[0])
                        elif ',' in resRoomType: # Single Bed Room is always at the front
                            numSingle = int(resRoomType.split(',')[0].split()[0]) # [2 x Single Bed Room, 3 x Twin Bed Room]: numSingle = 2
                    if 'Twin Bed Room' in resRoomType:
                        if 'x' not in resRoomType and ',' not in resRoomType: # [Twin Bed Room]: numTwin = 1
                            numTwin = 1
                        elif 'x' in resRoomType and ',' not in resRoomType: # [2 x Twin Bed Room]: numTwin = 2
                            numTwin = int(resRoomType.split()[0])
                        elif ',' in resRoomType: # Twin Bed Room is always at the back
                            numTwin = int(resRoomType.split(',')[1].split()[0]) # [2 x Single Bed Room, 3 x Twin Bed Room]: numTwin = 3

                    if row[9] == 'Smart Flex':
                        row[5] = row[9] # place row 9 into row 5 - row 5 is always empty is 'Smart Flex' is in row 9
                        
                    convertedCheckInDate = datetime.strptime(row[2], '%d-%b-%y')
                    convertedCheckOutDate = datetime.strptime(row[3], '%d-%b-%y')
                    
                    # create a new bookingcom reservation object using the extracted data
                    importBookingcomRes = bookingcomReservations.objects.create(
                        guestName=row[0],
                        numGuests=row[1],
                        checkInDate=convertedCheckInDate,
                        checkOutDate=convertedCheckOutDate,
                        numSingle=numSingle,
                        numTwin=numTwin,
                        totalPayment=row[6],
                        commission=row[7],
                        extReservationId=row[8],
                        reservationStatus=row[9],
                        listedWebsites = bookingWebsite.objects.get(websiteName = "Booking.com"),
                        importTime=timezone.now(),
                    )
                    
                    # save the object
                    importBookingcomRes.save()