from django.http import HttpRequest
from django.test import TestCase

from sh8core.models import Mail
from sh8core.readauth import ReadAuthorityChecker, CannotReadReasons


class ReadAuthorityCheckerTest(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.session = {
            'recipient': 'ggone'
        }
        self.secret_code = 'chinatown'

    def test_can_read(self):
        self.request.POST['secret_code'] = self.secret_code
        mail = Mail.objects.create(recipient='ggone', sender='gil@wtf.com',
                                   contents='hello sidney..',
                                   secret_code=self.secret_code)
        checker = ReadAuthorityChecker(self.request, mail)

        self.assertEqual(checker.check(), (True, None))

    def test_cannot_read__secretcode(self):
        self.request.POST['secret_code'] = 'wrong_secret_code'
        mail = Mail.objects.create(recipient='ggone', sender='gil@wtf.com',
                                   contents='hello sidney..',
                                   secret_code=self.secret_code)
        checker = ReadAuthorityChecker(self.request, mail)

        self.assertEqual(checker.check(),
                         (False, {CannotReadReasons.secret_code}))
