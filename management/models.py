from django.db import models


class Room(models.Model):
    SINGLE_ROOM_REF = 'si'
    DOUBLE_ROOM_REF = 'do'
    SUITE_ROOM_REF = 'su'

    ROOM_CHOICES = (
        (SINGLE_ROOM_REF, 'Single'),
        (DOUBLE_ROOM_REF, 'Double'),
        (SUITE_ROOM_REF, 'Suite')
    )
    room_number = models.IntegerField(unique=True)
    room_type = models.CharField(choices=ROOM_CHOICES, max_length=2)
    price_per_night = models.DecimalField(decimal_places=2, max_digits=10)
