import logging
from datetime import datetime

from rest_framework.generics import CreateAPIView, DestroyAPIView

from customer.exceptions import (
    RoomObjectNotExists, RoomAlreadyReserved, ReservationNotExists,
    ReservationCantBeCancelledDueToReservationStart
)
from customer.models import RoomReservation
from customer.serializers import CreateUserSerializer, CreateRoomReservationSerializer
from management.models import Room

logger = logging.getLogger(__name__)


class CreateUserApi(CreateAPIView):
    serializer_class = CreateUserSerializer
    authentication_classes = []


class RoomReservationApi(CreateAPIView):
    serializer_class = CreateRoomReservationSerializer

    @staticmethod
    def check_has_no_reservation_in_requested_date(serializer, room):
        from_date = serializer.validated_data.get('from_date')
        to_date = serializer.validated_data.get('to_date')
        room_reservation_exists = room.all_reservations.filter(from_date__gte=from_date, to_date__lte=to_date)
        if room_reservation_exists:
            raise RoomAlreadyReserved()

    def get_room(self):
        pk = self.kwargs.get('pk')
        room = Room.objects.filter(pk=pk).first()
        if not room:
            logger.debug(f'<{self.request.user}> cant reserve room due to room: {pk} not exists')
            raise RoomObjectNotExists()
        return room

    def perform_create(self, serializer):
        room = self.get_room()
        self.check_has_no_reservation_in_requested_date(serializer, room)
        serializer.save(room=room)


class RoomReservationCancelApi(DestroyAPIView):

    def get_object(self):
        pk = self.kwargs.get('pk')
        room_reservation = RoomReservation.objects.filter(pk=pk).first()
        if not room_reservation:
            logger.warning(f'<{self.request.user}> cant cancel reservation: {pk} not exists')
            raise ReservationNotExists()

        if room_reservation.from_date == datetime.now().date():
            logger.warning(f'<{self.request.user}> cant cancel reservation: {pk} due to start_date')
            raise ReservationCantBeCancelledDueToReservationStart()

        return room_reservation
