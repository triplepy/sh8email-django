from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from .exceptions import BackdoorIntendedError


class BackdoorTest(TestCase):
    def test_raise_error_success_case(self):
        with self.assertRaises(BackdoorIntendedError):
            self.client.post(reverse('backdoor:raise_error'), {
                'key': settings.BACKDOOR_KEY
            })

    def test_raise_error_without_key(self):
        response = self.client.post(reverse('backdoor:raise_error'))
        self.assertContains(response, 'Please input key via POST method.')

    def test_raise_error_with_wrong_key(self):
        response = self.client.post(reverse('backdoor:raise_error'), {
            'key': 'wrong_key'
        })
        self.assertContains(response, 'Wrong key.')
