class CheckinManager(object):
    def __init__(self, request):
        self.request = request

    def current_recipient(self):
        return self.request.session.get('recipient')

    def checkin(self, recipient):
        self.request.session['recipient'] = recipient


class MockCheckinManager(CheckinManager):
    def __init__(self, recipient):
        self.recipient = recipient

    def current_recipient(self):
        return self.recipient

    def checkin(self, recipient):
        self.recipient = recipient
