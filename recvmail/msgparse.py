import re
from email.header import decode_header, make_header
from email.message import EmailMessage
from email.parser import Parser
from email.utils import parseaddr, formataddr

from sh8core.models import Mail


# TODO REGEX 보완 필요
CHARSET_IN_CONTENTTYPE_REGEX = re.compile("charset=(.+)$")


def raw_to_mail(rawtext):
    msg = Parser(_class=EmailMessage).parsestr(rawtext)

    sender = readablize_header(msg.get('From'))
    subject = readablize_header(msg.get('Subject'))

    address = Address(header_to=msg.get('To'))

    body = msg.get_body(preferencelist=('html', 'plain'))
    _try_set_charset_smarter(body)

    contents = str(body.get_payload(decode=True),
                   encoding=str(body.get_charset()))

    mail = Mail(recipient=address.recipient,
                secret_code=address.secret_code,
                sender=sender,
                subject=subject,
                contents=contents,)

    return mail


def _try_set_charset_smarter(body):
    if body.get_charset() is None:
        content_type = body['Content-Type']
        if content_type:
            charset = CHARSET_IN_CONTENTTYPE_REGEX.search(content_type).group(1)
        else:
            charset = 'utf-8'  # Use default charset.
        body.set_charset(charset)


def readablize_header(header):
    return str(make_header(decode_header(header)))


def reproduce_mail(origin, rcpttos):
    rcpttos_filtered = [r for r in rcpttos if '@sh8.email' in r]
    mails = []
    for rcptto in rcpttos_filtered:
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
