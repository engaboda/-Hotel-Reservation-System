from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from customer.models import RoomReservation
from hotel.base_test import BaseTest
from management.models import Room

User = get_user_model()


class TestJwtApis(TestCase):
    def setUp(self):
        self.password = '1234'
        self.user = User.objects.create(
            username='test', is_active=True
        )
        self.user.set_password(self.password)
        self.user.save()

        self.get_token_url = reverse('token_obtain_pair')
        self.get_refresh_token_url = reverse('token_refresh')

    def test_get_token(self):
        data = {
            'username': self.user.username,
            'password': self.password
        }
        response = self.client.post(self.get_token_url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('refresh'))
        self.assertIsNotNone(response.data.get('access'))

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_get_refresh_token(self):
        data = {
            'refresh': self.get_tokens_for_user(self.user)['refresh']
        }
        response = self.client.post(self.get_refresh_token_url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('access'))


class TestCreateUser(TestCase):
    def setUp(self):
        self.create_user_url = reverse('customer:customer-create')

    def test_create_customer(self):
        data = {
            'username': 'aboda',
            'password': '1234'
        }
        create_user_response = self.client.post(self.create_user_url, data)
        self.assertEquals(create_user_response.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(username=data.get('username')).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(data.get('password')))


class TestCustomerReserveRoom(BaseTest):

    def setUp(self):
        self.room = Room.objects.create(**{
            "room_number": 10, 'room_type': Room.SINGLE_ROOM_REF, 'price_per_night': 10
        })
        self.admin_user = User.objects.create_user(
            username='admin', password='1234', is_staff=True
        )
        self.client = TestCase.client_class()
        self.create_room_reservation_url = reverse('customer:reserve_room', kwargs={'pk': self.room.pk})

    def test_reserve_room_success(self):
        data = {
            'from_date': datetime.now().date(),
            'to_date': (datetime.now() + timedelta(days=3)).date()
        }

        headers = {
            'Authorization': f'Bearer {self.get_tokens_for_user(self.admin_user).access_token}'
        }

        create_room_reservation_response = self.client.post(self.create_room_reservation_url, data, headers=headers)
        self.assertEquals(create_room_reservation_response.status_code, 201)
        room_reservation = RoomReservation.objects.filter(room=self.room).first()
        self.assertIsNotNone(room_reservation)
        self.assertEquals(room_reservation.from_date, data['from_date'])
        self.assertEquals(room_reservation.to_date, data['to_date'])

    def test_reserve_room_failure_due_to_reserved(self):
        RoomReservation.objects.create(**{
            "room": self.room, 'from_date': datetime.now().date(),
            'to_date': datetime.now().date() + timedelta(days=3)
        })
        data = {
            'from_date': datetime.now().date(),
            'to_date': (datetime.now() + timedelta(days=3)).date()
        }

        headers = {
            'Authorization': f'Bearer {self.get_tokens_for_user(self.admin_user).access_token}'
        }

        create_room_reservation_response = self.client.post(self.create_room_reservation_url, data, headers=headers)
        self.assertEquals(create_room_reservation_response.status_code, 422)
        self.assertEquals(create_room_reservation_response.data['detail'], 'Room already reserved.')


class TestCustomerCancelReservationRoom(BaseTest):

    def setUp(self):
        self.room = Room.objects.create(**{
            "room_number": 10, 'room_type': Room.SINGLE_ROOM_REF, 'price_per_night': 10
        })
        self.room_reservation = RoomReservation.objects.create(**{
            "room": self.room, 'from_date': datetime.now().date(),
            'to_date': datetime.now().date() + timedelta(days=3)
        })
        self.admin_user = User.objects.create_user(
            username='admin', password='1234', is_staff=True
        )

    def test_cancel_reserve_room_not_able_due_to_start_date_of_reservation_is_current_date(self):
        self.delete_room_reservation_url = reverse(
            'customer:cancel_room_reservations', kwargs={'pk': self.room_reservation.pk})
        headers = {
            'Authorization': f'Bearer {self.get_tokens_for_user(self.admin_user).access_token}'
        }

        create_room_reservation_response = self.client.delete(self.delete_room_reservation_url, headers=headers)
        self.assertEquals(create_room_reservation_response.status_code, 422)
        room_reservation = RoomReservation.objects.filter(room=self.room).first()
        self.assertIsNotNone(room_reservation)

    def test_cancel_reserve_room_success(self):
        room = Room.objects.create(**{
            "room_number": 1, 'room_type': Room.SINGLE_ROOM_REF, 'price_per_night': 1
        })
        room_reservation = RoomReservation.objects.create(**{
            "room": room, 'from_date': datetime.now().date() + timedelta(days=1),
            'to_date': datetime.now().date() + timedelta(days=3)
        })

        self.delete_room_reservation_url = reverse(
            'customer:cancel_room_reservations', kwargs={'pk': room_reservation.pk})

        headers = {
            'Authorization': f'Bearer {self.get_tokens_for_user(self.admin_user).access_token}'
        }

        create_room_reservation_response = self.client.delete(self.delete_room_reservation_url, headers=headers)
        self.assertEquals(create_room_reservation_response.status_code, 204)
        room_reservation = RoomReservation.objects.filter(room=room).first()
        self.assertIsNone(room_reservation)
