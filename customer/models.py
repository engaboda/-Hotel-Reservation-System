from django.db import models
from management.models import Room


class RoomReservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='all_reservations')
    from_date = models.DateField()
    to_date = models.DateField()
