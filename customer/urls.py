from django.urls import path

from customer.viewsets import CreateUserApi, RoomReservationApi, RoomReservationCancelApi

urlpatterns = [
    path('customer/', CreateUserApi.as_view(), name='customer-create'),
    path('rooms/<int:pk>', RoomReservationApi.as_view(), name='reserve_room'),
    path('room_reservations/<int:pk>', RoomReservationCancelApi.as_view(), name='cancel_room_reservations')
]
