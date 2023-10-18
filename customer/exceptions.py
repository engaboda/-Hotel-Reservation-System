from rest_framework.exceptions import APIException


class RoomObjectNotExists(APIException):
    status_code = 404
    default_detail = 'Room objects not available.'
    default_code = 'room_objects_not_available'


class RoomAlreadyReserved(APIException):
    status_code = 422
    default_detail = 'Room already reserved.'
    default_code = 'room_reserved'


class ReservationNotExists(APIException):
    status_code = 404
    default_detail = 'Room Reservation not exists.'
    default_code = 'room_reservation_not_exists'


class ReservationCantBeCancelledDueToReservationStart(APIException):
    status_code = 422
    default_detail = 'Room Reservation cant be canceled due to reservation start.'
    default_code = 'room_reservation_not_exists'
