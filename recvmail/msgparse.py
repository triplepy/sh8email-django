from email.header import decode_header, make_header
from email.message import EmailMessage
from email.parser import Parser
from email.utils import parseaddr

from front.models import Mail
from recvmail.util import extract_recipient, is_secret, extract_secretcode


def raw_to_mail(rawtext):
    msg = Parser(_class=EmailMessage).parsestr(rawtext)

    sender = str(make_header(decode_header(msg.get('From'))))
    subject = str(make_header(decode_header(msg.get('Subject'))))

    mail = Mail(recipient=extract_recipient(msg),
                secret_code=extract_secretcode(msg),
                sender=sender,
                subject=subject,
                contents=msg.get_body().get_payload())

    return mail


def reproduce_mail(origin, rcpttos):
    mails = []
    for rcptto in rcpttos:
        recipient = extract_recipient(rcptto)
        m = Mail(
                recipient=recipient,
                # TODO refactor
                secret_code=extract_secretcode(rcptto.split('@')[0]),
                sender=origin.sender,
                subject=origin.subject,
                contents=origin.subject
        )
        mails.append(m)
    return mails
