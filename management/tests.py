from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from customer.models import RoomReservation
from hotel.base_test import BaseTest
from management.models import Room

User = get_user_model()


class TestListCreateRoom(BaseTest):

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin-1', password='1234', is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='normal', password='1234', is_staff=False, is_superuser=False
        )
        self.list_create_room_url = reverse('management:room-create-list')

        rooms = Room.objects.bulk_create(
            [
                Room(**{"room_number": 10, 'room_type': Room.SINGLE_ROOM_REF, 'price_per_night': 10}),
                Room(**{"room_number": 20, 'room_type': Room.SUITE_ROOM_REF, 'price_per_night': 20}),
                Room(**{"room_number": 30, 'room_type': Room.DOUBLE_ROOM_REF, 'price_per_night': 30}),
            ]
        )
        RoomReservation.objects.create(
            room=rooms[0], from_date=datetime.now().date(), to_date=datetime.now().date() + timedelta(days=3)
        )

    def test_create_room(self):
        data = {
            'room_number': 1,
            'room_type': Room.SINGLE_ROOM_REF,
            'price_per_night': 10
        }
        headers = {
            'Authorization': f'Bearer {self.get_tokens_for_user(self.admin_user).access_token}'
        }
        create_room_response = self.client.post(self.list_create_room_url, data, headers=headers)

        self.assertEquals(create_room_response.status_code, status.HTTP_201_CREATED)
        room = Room.objects.filter(room_number=data.get('room_number')).first()
        self.assertIsNotNone(room)
        self.assertEquals(room.room_number, data['room_number'])
        self.assertEquals(room.room_type, data['room_type'])
        self.assertEquals(room.price_per_night, data['price_per_night'])

    def test_create_room_using_normal_user(self):
        data = {
            'room_number': 1,
            'room_type': Room.SINGLE_ROOM_REF,
            'price_per_night': 10
        }
        headers = {
            'Authorization': f'Bearer {self.get_tokens_for_user(self.normal_user).access_token}'
        }
        create_room_response = self.client.post(self.list_create_room_url, data, headers=headers)

        self.assertEquals(create_room_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(create_room_response.data['detail'], 'not-allowed')

    def test_list_rooms(self):
        needed_date = datetime.now().date() + timedelta(days=2)
        list_room_response = self.client.get(self.list_create_room_url+f'?date={needed_date}')
        self.assertEquals(list_room_response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            len(list_room_response.data),
            2,
            'because there are 3 rooms created using bulk command but one of them will be available after 3 days'
        )

        self.assertEquals(list_room_response.data[0]['room_number'], 30)
        self.assertEquals(list_room_response.data[0]['room_type'], Room.DOUBLE_ROOM_REF)
        self.assertEquals(list_room_response.data[0]['price_per_night'], '30.00')
