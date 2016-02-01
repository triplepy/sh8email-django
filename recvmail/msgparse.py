from email.header import decode_header, make_header
from email.message import EmailMessage
from email.parser import Parser
from email.utils import parseaddr, formataddr

from front.models import Mail


def raw_to_mail(rawtext):
    msg = Parser(_class=EmailMessage).parsestr(rawtext)

    sender = readablize_header(msg.get('From'))
    subject = readablize_header(msg.get('Subject'))

    address = Address(header_to=msg.get('To'))

    mail = Mail(recipient=address.recipient,
                secret_code=address.secret_code,
                sender=sender,
                subject=subject,
                contents=msg.get_body().get_payload())

    return mail


def readablize_header(header):
    return str(make_header(decode_header(header)))


def reproduce_mail(origin, rcpttos):
    mails = []
    for rcptto in rcpttos:
        address = Address(header_to=rcptto)
        m = Mail(
                recipient=address.recipient,
                secret_code=address.secret_code,
                sender=origin.sender,
                subject=origin.subject,
                contents=origin.subject
        )
        mails.append(m)
    return mails


class Address(object):
    def __init__(self, local=None, domain=None, name='Name', header_to=None):
        self.local = local
        self.domain = domain
        self.name = name

        if header_to:
            self.name, address_str = parseaddr(header_to)
            self.local, self.domain = address_str.split('@')

    @property
    def recipient(self):
        return self._split_local()[0]

    @property
    def secret_code(self):
        return self._split_local()[1]

    def _split_local(self):
        if self._is_secret(self.local):
            recipient, secret_code = self.local.split('$$')
            return recipient, secret_code
        else:
            return self.local, self.local

    def _is_secret(self, local):
        return '$$' in local

    def as_str(self):
        return self.local + '@' + self.domain

    def as_headerstr(self):
        return formataddr((self.name, self.as_str()))

    def __str__(self):
        return self.as_str()
