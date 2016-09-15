from email.header import decode_header, make_header
from email.message import EmailMessage
from email.parser import Parser
from email.utils import parseaddr, formataddr

from sh8core.models import Mail


def raw_to_mail(rawtext):
    msg = Parser(_class=EmailMessage).parsestr(rawtext)

    sender = readablize_header(msg.get('From'))
    subject = readablize_header(msg.get('Subject'))

    address = Address(header_to=msg.get('To'))

    contents = str(msg.get_body(preferencelist=('html', 'plain'))
                      .get_payload(decode=True),
                   encoding='utf-8')

    mail = Mail(recipient=address.recipient,
                secret_code=address.secret_code,
                sender=sender,
                subject=subject,
                contents=contents,)

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
                contents=origin.contents,
        )
        mails.append(m)
    return mails


class Address(object):
    secret_code_sep = '__'

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
            recipient, secret_code = self.local.split(self.secret_code_sep)
            return recipient, secret_code
        else:
            return self.local, None

    def _is_secret(self, local):
        return self.secret_code_sep in local

    def as_str(self):
        return self.local + '@' + self.domain

    def as_headerstr(self):
        return formataddr((self.name, self.as_str()))

    def __str__(self):
        return self.as_str()
