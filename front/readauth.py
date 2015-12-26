from front.checkin import CheckinManager


class ReadAuthorityChecker(object):
    def __init__(self, request, mail):
        self.request = request
        self.mail = mail

    def check(self):
        checkin_manager = CheckinManager(self.request)
        secret_code = self.request.POST.get('secret_code')

        return self.mail.is_own(checkin_manager) and \
               self._check_secretcode_equality(secret_code)

    def _check_secretcode_equality(self, secret_code):
        return secret_code == self.mail.secret_code
