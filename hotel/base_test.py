from django.test import TestCase

from rest_framework_simplejwt.tokens import RefreshToken


class BaseTest(TestCase):

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return refresh
