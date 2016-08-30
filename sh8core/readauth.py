from enum import Enum

from sh8core.checkin import CheckinManager


class CannotReadReasons(Enum):
    secret_code = 1
    recipient = 2


class ReadAuthorityChecker(object):
    def __init__(self, request, mail):
        self.request = request
        self.mail = mail
        self.checkin_manager = CheckinManager(self.request)

    def check(self):
        secret_code = self.request.POST.get('secret_code')

        is_own = self.mail.is_own(self.checkin_manager)
        secret_code_match = self._check_secretcode_equality(secret_code)

        if is_own and secret_code_match:
            return True, None
        elif is_own and not secret_code_match:
            return False, {CannotReadReasons.secret_code}
        elif not is_own and secret_code_match:
            return False, {CannotReadReasons.recipient}
        elif not is_own and not secret_code_match:
            return False, {CannotReadReasons.secret_code, CannotReadReasons.recipient}
        else:
            raise AssertionError('Happen which is cannot!')

    def _check_secretcode_equality(self, secret_code):
        return secret_code == self.mail.secret_code
