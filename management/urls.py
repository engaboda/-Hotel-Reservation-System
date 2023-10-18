from django.urls import path

from management.viewsets import ListCreateRoomApi

urlpatterns = [
    path('rooms/', ListCreateRoomApi.as_view(), name='room-create-list'),
]
